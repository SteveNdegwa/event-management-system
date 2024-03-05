import dateparser
import uuid
import cloudinary
import pybase64
from cloudinary.uploader import upload
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from base.backend.ServiceLayer import StateService
from invites.views import invite_to_event
from services.decorators import verify_token
from user_management.backend.ServiceLayer import CachedUserService
from .backend.ServiceLayer import EventTypeService, EventService, AttendeeService, RoleService, TicketService
from services.request_processor import get_request_data
from logs.views import TransactionLog
from notifications.views import create_notification
from datetime import datetime


# convert event object to a dictionary
@csrf_exempt
def events_to_list(events):
    data = {}
    event_list = list()
    for item in events:
        today = datetime.now()
        if today.date() > item.end.date():
            completed_state = StateService().get(name="completed")
            EventService().update(item.uuid, event_state=completed_state)

        data = {'uuid': item.uuid, 'name': item.name, 'description': item.description, 'creator_id': item.creator_id,
                'start': item.start, 'end': item.end, 'venue': item.venue, 'price': item.price,
                'capacity': item.capacity, 'image': item.image, 'event_type': item.event_type.name,
                'event_state': item.event_state.name}
        event_list.append(data)

    return event_list


@csrf_exempt
def get_events(request):
    try:
        active_state = StateService().get(name='active')
        events = EventService().filter(event_state=active_state)
        event_list = events_to_list(events)
        return JsonResponse({"events": event_list, "code": "200"})
    except:
        return JsonResponse({"message": "Internal server error", "code": "500"})


@csrf_exempt
def get_upcoming_events(request):
    try:
        active_state = StateService().get(name='active')
        current_time = datetime.now()
        events = EventService().filter(event_state=active_state, start__gte=current_time).order_by("start")[:5]
        event_list = events_to_list(events)
        return JsonResponse({"events": event_list, "code": "200"})
    except:
        return JsonResponse({"message": "Internal server error", "code": "500"})


@csrf_exempt
def get_ongoing_events(request):
    try:
        active_state = StateService().get(name='active')
        current_time = datetime.now()
        events = EventService().filter(event_state=active_state, start__lte=current_time,
                                       end__gte=current_time).order_by("start")[:5]
        event_list = events_to_list(events)
        return JsonResponse({"events": event_list, "code": "200"})
    except:
        return JsonResponse({"message": "Internal server error", "code": "500"})


@csrf_exempt
def get_created_events(request):
    try:
        data = get_request_data(request)
        user_id = data.get('user_id')
        deleted_state = StateService().get(name='deleted')
        events = EventService().filter(creator_id=user_id).exclude(event_state=deleted_state)
        event_list = events_to_list(events)
        return JsonResponse({"events": event_list, "code": "200"})
    except:
        return JsonResponse({"message": "Internal server error", "code": "500"})


@csrf_exempt
def get_booked_events(request):
    try:
        data = get_request_data(request)
        user_id = data.get('user_id')

        user = CachedUserService().get(user_id=user_id)
        active_state = StateService().get(name='active')
        attendees = AttendeeService().filter(user=user, attendee_state=active_state)

        event_list = list()
        for item in attendees:
            data = {'uuid': item.event.uuid, 'name': item.event.name, 'description': item.event.description,
                    'creator_id': item.event.creator_id, 'start': item.event.start, 'end': item.event.end,
                    'venue': item.event.venue, 'price': item.event.price, 'capacity': item.event.capacity,
                    'image': item.event.image, 'event_type': item.event.event_type.name,
                    'event_state': item.event.event_state.name}
            event_list.append(data)
        return JsonResponse({"events": event_list, "code": "200"})
    except:
        return JsonResponse({"message": "Internal server error", "code": "500"})


@csrf_exempt
def get_event_by_id(request):
    try:
        data = get_request_data(request)
        event_id = data.get('event_id')
        event = EventService().filter(uuid=event_id)
        event_list = events_to_list(event)
        return JsonResponse({"events": event_list, "code": "200"})
    except:
        return JsonResponse({"message": "Internal server error", "code": "500"})


@csrf_exempt
def search_events(request):
    try:
        data = get_request_data(request)
        search = data.get('search')
        active_state = StateService().get(name='active')

        events = EventService().filter(name__contains=search, event_state=active_state) | EventService().filter(
            description__contains=search, event_state=active_state) | EventService().filter(
            creator_id__contains=search, event_state=active_state) | EventService().filter(start__contains=search,
                                                                                           event_state=active_state) | EventService().filter(
            end__contains=search, event_state=active_state) | EventService().filter(venue__contains=search,
                                                                                    event_state=active_state) | EventService().filter(
            price__contains=search, event_state=active_state) | EventService().filter(capacity__contains=search,
                                                                                      event_state=active_state)

        event_list = events_to_list(events)
        return JsonResponse({"events": event_list, "code": "200"})
    except:
        return JsonResponse({"message": "Internal server error", "code": "500"})


@csrf_exempt
def get_event_types(request):
    try:
        data = get_request_data(request)

        active_state = StateService().get(name='active')
        types = EventTypeService().filter(event_type_state=active_state)

        event_types_list = list()
        for item in types:
            event_types_list.append(item.name)
        return JsonResponse({"event_types": event_types_list, "code": "200"})

    except:
        return JsonResponse({"message": "Internal server error", "code": "500"})


@csrf_exempt
@verify_token
def create_event(request):
    transaction_log = TransactionLog()
    try:
        data = get_request_data(request)
        user_id = data.get('user_id')
        start_time = dateparser.parse(data.get('start')).date()
        end_time = dateparser.parse(data.get('end')).date()

        transaction_log.start_transaction(user_id, 'create_event', data)

        try:
            decoded_image_data = pybase64.b64decode(data.get('image'))
            random_filename = uuid.uuid4().hex + "events"
            upload_result = cloudinary.uploader.upload(
                file=decoded_image_data,
                public_id=random_filename,
                resource_type="image",
            )
        except:
            response = {"message": "Error uploading image", "code": "500"}
            transaction_log.complete_transaction(response, False)
            return JsonResponse(response)

        today = datetime.now()
        if end_time < start_time or start_time < today.date():
            response = {"message": "Invalid event timelines", "code": "500"}
            transaction_log.complete_transaction(response, False)
            return JsonResponse(response)

        event_state = StateService().get(name='active')
        event_type = EventTypeService().get(name=data.get('event_type'))

        event = EventService().create(
            name=data.get('name'),
            description=data.get('description'),
            creator_id=user_id,
            start=data.get('start'),
            end=data.get('end'),
            venue=data.get('venue'),
            capacity=data.get('capacity'),
            price=data.get('price'),
            image=upload_result['secure_url'],
            event_type=event_type,
            event_state=event_state,
        )

        # create default role
        role_state = StateService().get(name="active")
        role = RoleService().create(name="attendee", description="attendee", role_event=event, role_state=role_state)

        # response
        response = {"message": "Event created successfully", "code": "201"}
        transaction_log.complete_transaction(response, True)

        create_notification(user_id, "Event created",
                            f"You created an event: {data.get('name')} - {data.get('description')}")

        return JsonResponse(response)
    except:
        response = {"message": "Internal server error", "code": "500"}
        transaction_log.complete_transaction(response, False)
        return JsonResponse(response)


@csrf_exempt
@verify_token
def update_event(request):
    transaction_log = TransactionLog()
    try:
        data = get_request_data(request)
        event_id = data.get('event_id')
        user_id = data.get('user_id')
        start_time = dateparser.parse(data.get('start')).date()
        end_time = dateparser.parse(data.get('end')).date()

        event = EventService().get(uuid=event_id)

        transaction_log.start_transaction(user_id, 'update_event', data)


        try:
            decoded_image_data = pybase64.b64decode(data.get('image'))
            random_filename = uuid.uuid4().hex + "events"
            upload_result = cloudinary.uploader.upload(
                file=decoded_image_data,
                public_id=random_filename,
                resource_type="image",
            )
        except:
            response = {"message": "Error uploading image", "code": "500"}
            transaction_log.complete_transaction(response, False)
            return JsonResponse(response)

        today = datetime.now()
        if end_time < start_time or start_time < today.date():
            response = {"message": "Invalid event timelines", "code": "500"}
            transaction_log.complete_transaction(response, False)
            return JsonResponse(response)

        if user_id != str(event.creator_id):
            response = {"message": "Not authorised to perform this operation", "code": "403"}
            transaction_log.complete_transaction(response, False)
            return JsonResponse(response)

        event_type = EventTypeService().get(name=data.get('event_type'))
        state = StateService().get(name='active')
        EventService().update(
            event_id,
            name=data.get('name'),
            description=data.get('description'),
            start=data.get('start'),
            end=data.get('end'),
            venue=data.get('venue'),
            capacity=data.get('capacity'),
            price=data.get('price'),
            image=upload_result['secure_url'],
            event_type=event_type,
            event_state=state,
        )

        response = {"message": "Event updated successfully", "code": "200"}
        transaction_log.complete_transaction(response, True)

        create_notification(user_id, "Event Updated",
                            f"Event: '{data.get('name')}' - '{data.get('description')}' updated successfully")

        return JsonResponse(response)


    except:
        response = {"message": "Internal server error", "code": "500"}
        transaction_log.complete_transaction(response, False)
        return JsonResponse(response)


@csrf_exempt
@verify_token
def delete_event(request):
    transaction_log = TransactionLog()
    try:
        data = get_request_data(request)
        user_id = data.get('user_id')
        event_id = data.get('event_id')

        # start transaction
        transaction_log.start_transaction(user_id, 'delete_event', data)

        # get event to be deleted
        event = EventService().get(uuid=event_id)

        # check if user is event creator
        creator_id = event.creator_id
        if str(user_id) != str(creator_id):
            response = {"message": "You are not authorized to perform this transaction", "code": "403"}
            transaction_log.complete_transaction(response, False)
            return JsonResponse(response)

        # get deleted state
        deleted_state = StateService().get(name="deleted")

        # delete event
        EventService().update(event_id, event_state=deleted_state)

        # get affected attendees and inactivate them
        affected_attendees = AttendeeService().filter(event=event)
        incative_state = StateService().get(name="inactive")
        for attendee in affected_attendees:
            AttendeeService().update(attendee.uuid, attendee_state=incative_state)
            ticket = TicketService().get(ticket_attendee=attendee.uuid)
            TicketService().update(ticket.uuid, ticket_state=incative_state)
            create_notification(attendee.user.user_id, name="Event Cancelled",
                                description=f"Event: '{event.name} - {event.description}' was cancelled. Sorry for any inconveniences caused")

        # complete transaction
        response = {"message": "Event deleted successfully", "code": "200"}
        transaction_log.complete_transaction(response, True)

        # create notification
        create_notification(user_id, name="Event deleted",
                            description=f"Event: {event.name} - {event.description} deleted successfully")

        return JsonResponse(response)

    except:
        response = {"message": "Internal server error", "code": "500"}
        transaction_log.complete_transaction(response, False)
        return JsonResponse(response)


@csrf_exempt
@verify_token
def invite(request):
    return invite_to_event(request)


@csrf_exempt
@verify_token
def attend_event(request):
    # initialize transaction
    transaction_log = TransactionLog()
    try:
        data = get_request_data(request)
        user_id = data.get('user_id')
        event_id = data.get('event_id')

        # start transaction
        transaction_log.start_transaction(user_id, 'attend_event', data)

        # get the event instance
        event = EventService().get(uuid=event_id)

        # get event capacity and check if there's remaining slots
        event_capacity = int(event.capacity)
        if event_capacity < 2:
            response = {"message": "Event is full", "code": "200"}
            transaction_log.complete_transaction(response, False)
            return JsonResponse(response)

        # get active state instance
        attendee_state = StateService().get(name="active")

        # get attendee role instance
        role = RoleService().get(name="attendee", role_event=event)
        user = CachedUserService().get(user_id=user_id)

        # create attendee
        attendee = AttendeeService().create(user=user, event=event, role=role, attendee_state=attendee_state)

        # update event capacity
        EventService().update(event.uuid, capacity=event_capacity - 1)

        # create ticket
        ticket = create_ticket(user_id, str(attendee.uuid))

        # create notification
        create_notification(user_id, name="Event booked",
                            description=f"Event: '{event.name}' - '{event.description}' booked successfully. Ticket Id: '{ticket.uuid}'")

        response = {"message": "Event booked successfully", "code": "201", "ticket_id": ticket.uuid}
        transaction_log.complete_transaction(response, True)
        return JsonResponse(response)


    except:
        response = {"message": "Internal server error", "code": "500"}
        transaction_log.complete_transaction(response, False)
        return JsonResponse(response)


@csrf_exempt
@verify_token
def unbook_event(request):
    # initialize transaction
    transaction_log = TransactionLog()
    try:
        data = get_request_data(request)
        user_id = data.get('user_id')
        event_id = data.get('event_id')

        # start transaction
        transaction_log.start_transaction(user_id, 'unbook_event', data)

        # get the event instance
        event = EventService().get(uuid=event_id)

        # get user
        user = CachedUserService().get(user_id=user_id)

        # get active state instance
        active_state = StateService().get(name="active")

        # get attendee
        attendee = AttendeeService().get(user=user, event=event, attendee_state=active_state)

        # get inactive state instance
        inactive_state = StateService().get(name="inactive")

        # update attendee
        AttendeeService().update(attendee.uuid, attendee_state=inactive_state)

        # update event capacity
        event_capacity = int(event.capacity)
        EventService().update(event.uuid, capacity=event_capacity + 1)

        # update ticket
        ticket = TicketService().get(ticket_attendee=attendee)
        TicketService().update(ticket.uuid, ticket_state=inactive_state)

        # create notification
        create_notification(user_id, name="Event unbooked",
                            description=f"Event: '{event.name}' - '{event.description}' unbooked successfully")

        response = {"message": "Event unbooked successfully", "code": "200"}
        transaction_log.complete_transaction(response, True)
        return JsonResponse(response)


    except:
        response = {"message": "Internal server error", "code": "500"}
        transaction_log.complete_transaction(response, False)
        return JsonResponse(response)


@csrf_exempt
def get_attendees(request):
    try:
        data = get_request_data(request)
        event_id = data.get('event_id')
        active_state = StateService().get(name='active')
        event = EventService().get(uuid=event_id)
        attendees = AttendeeService().filter(event=event, attendee_state=active_state)
        data = {}
        attendee_list = list()
        for item in attendees:
            data['uuid'] = item.uuid
            data['username'] = item.user.username
            data['role'] = item.role.name
            attendee_list.append(data)
            data = {}
        return JsonResponse({"attendees": attendee_list, "code": "200"})
    except:
        return JsonResponse({"message": "Internal server error", "code": "500"})


@csrf_exempt
def search_attendee(request):
    try:
        data = get_request_data(request)
        user_id = data.get('user_id')
        event_id = data.get('event_id')
        print(data)

        active_state = StateService().get(name='active')
        event = EventService().get(uuid=event_id)
        user = CachedUserService().get(user_id=user_id)

        attendees = AttendeeService().filter(user=user, event=event, attendee_state=active_state)
        data = {}
        attendee_list = list()
        for item in attendees:
            data['uuid'] = item.uuid
            data['username'] = item.user.username
            data['role'] = item.role.name
            attendee_list.append(data)
            data = {}
        return JsonResponse({"attendees": attendee_list, "code": "200"})
    except:
        return JsonResponse({"message": "Internal server error", "code": "500"})


@csrf_exempt
def create_ticket(user_id, attendee_id):
    ticket_transaction_log = TransactionLog()
    try:
        ticket_transaction_log.start_transaction(user_id, "create_ticket",
                                                 {"user_id": user_id, "attendee_id": attendee_id})
        attendee = AttendeeService().get(uuid=attendee_id)
        ticket_state = StateService().get(name="active")
        ticket = TicketService().create(ticket_attendee=attendee, ticket_state=ticket_state)
        response = {"message": "Ticket created successfully", "code": "201"}
        ticket_transaction_log.complete_transaction(response, True)
        return ticket
    except:
        response = {"message": "Error creating ticket", "code": "500"}
        ticket_transaction_log.complete_transaction(response, False)


@csrf_exempt
@verify_token
def create_role(request):
    # initialize log
    transaction_log = TransactionLog()
    try:
        data = get_request_data(request)
        user_id = data.get('user_id')
        event_id = data.get('event_id')
        name = data.get('name')
        description = data.get('description')

        # start log
        transaction_log.start_transaction(user_id, "create_role", data)

        # check if user is the event creator
        event = EventService().get(uuid=event_id)

        if user_id != str(event.creator_id):
            response = {"message": "You are not authorized to perform this action", "code": "403"}
            transaction_log.complete_transaction(response, False)
            return JsonResponse(response)

        role_state = StateService().get(name="active")
        role = RoleService().create(name=name, description=description, role_event=event, role_state=role_state)
        print("role id", role.uuid)

        create_notification(user_id, "Role Created",
                            f"You created a role: {name} - {description} for event: {event.name} - {event.description}")

        response = {"message": "Role created successfully", "code": "201"}
        transaction_log.complete_transaction(response, True)
        return JsonResponse(response)

    except:
        response = {"message": "Internal server error", "code": "500"}
        transaction_log.complete_transaction(response, False)
        return JsonResponse(response)


@csrf_exempt
@verify_token
def update_role(request):
    transaction_log = TransactionLog()
    try:
        data = get_request_data(request)
        user_id = data.get('user_id')
        role_id = data.get('role_id')
        new_name = data.get('name')
        new_description = data.get('description')

        # start log
        transaction_log.start_transaction(user_id, "update_role", data)

        # get role instance
        role = RoleService().get(uuid=role_id)
        old_name = role.name
        old_description = role.description

        # check if user is the event creator
        if user_id != str(role.role_event.creator_id):
            response = {"message": "You are not authorized to perform this action", "code": "403"}
            transaction_log.complete_transaction(response, False)
            return JsonResponse(response)

        RoleService().update(role_id, name=new_name, description=new_description)

        create_notification(user_id, "Role Updated",
                            f"You updated role: {old_name} - {old_description} to  {new_name} - {new_description}")

        response = {"message": "Role updated successfully", "code": "200"}
        transaction_log.complete_transaction(response, True)
        return JsonResponse(response)

    except:
        response = {"message": "Internal server error", "code": "500"}
        transaction_log.complete_transaction(response, False)
        return JsonResponse(response)


@csrf_exempt
@verify_token
def delete_role(request):
    transaction_log = TransactionLog()
    try:
        data = get_request_data(request)
        user_id = data.get('user_id')
        role_id = data.get('role_id')

        # start log
        transaction_log.start_transaction(user_id, "delete_role", data)

        # get role instance
        role = RoleService().get(uuid=role_id)

        # check if user is the event creator
        if user_id != str(role.role_event.creator_id):
            response = {"message": "You are not authorized to perform this action", "code": "403"}
            transaction_log.complete_transaction(response, False)
            return JsonResponse(response)

        deleted_state = StateService().get(name="deleted")

        RoleService().update(role_id, role_state=deleted_state)

        create_notification(user_id, "Role Deleted",
                            f"You deleted role: {role.name} - {role.description}")

        # get attendees linked to the role and update to default
        default_role = RoleService().get(name="attendee", role_event=role.role_event)
        linked_attendees = AttendeeService().filter(role=role)
        for linked_attendee in linked_attendees:
            AttendeeService().update(linked_attendee.uuid, role=default_role)

        response = {"message": "Role deleted successfully", "code": "200"}
        transaction_log.complete_transaction(response, True)
        return JsonResponse(response)

    except:
        response = {"message": "Internal server error", "code": "500"}
        transaction_log.complete_transaction(response, False)
        return JsonResponse(response)


@csrf_exempt
@verify_token
def assign_role(request):
    # initialize log
    transaction_log = TransactionLog()
    try:
        data = get_request_data(request)
        user_id = data.get('user_id')
        attendee_id = data.get('attendee_id')
        role_id = data.get('role_id')

        # start transaction log
        transaction_log.start_transaction(user_id, "assign_role", data)

        # get role instance
        role = RoleService().get(uuid=role_id)
        # check if user is the event creator
        creator_id = str(role.role_event.creator_id)
        if user_id != creator_id:
            response = {"message": "You are not authorized to perform this action", "code": "403"}
            transaction_log.complete_transaction(response, False)
            return JsonResponse(response)

        # update attendee role
        AttendeeService().update(attendee_id, role=role)

        # get attendee instance
        attendee = AttendeeService().get(uuid=attendee_id)

        # send notifications
        create_notification(user_id, "Role Assigned",
                            f"You assigned a role: {role.name} - {role.description} for event: {role.role_event.name} - {role.role_event.description} to attendee: {attendee.user.username}")

        create_notification(attendee.user_id, "Role Assigned",
                            f"You were assigned a role: {role.name} - {role.description} for event: {role.role_event.name} - {role.role_event.description}")

        response = {"message": "Role assigned successfully", "code": "200"}
        transaction_log.complete_transaction(response, True)
        return JsonResponse(response)


    except:
        response = {"message": "Internal server error", "code": "500"}
        transaction_log.complete_transaction(response, False)
        return JsonResponse(response)


@csrf_exempt
@verify_token
def unassign_role(request):
    # initialize log
    transaction_log = TransactionLog()
    try:
        data = get_request_data(request)
        user_id = data.get('user_id')
        attendee_id = data.get('attendee_id')

        # start transaction log
        transaction_log.start_transaction(user_id, "unassign_role", data)

        # get role instance
        attendee = AttendeeService().get(uuid=attendee_id)
        role = RoleService().get(name="attendee", role_event=attendee.event)

        # check if user is the event creator
        creator_id = str(role.role_event.creator_id)
        if user_id != creator_id:
            response = {"message": "You are not authorized to perform this action", "code": "403"}
            transaction_log.complete_transaction(response, False)
            return JsonResponse(response)

        # update attendee role
        AttendeeService().update(attendee_id, role=role)

        # get attendee instance
        attendee = AttendeeService().get(uuid=attendee_id)

        # send notifications
        create_notification(user_id, "Role unassigned",
                            f"You unassigned a role: {role.name} - {role.description} for event: {role.role_event.name} - {role.role_event.description} to attendee: {attendee.user.username}")

        create_notification(attendee.user_id, "Role unassigned",
                            f"Your role: {role.name} - {role.description} for event: {role.role_event.name} - {role.role_event.description} was unassigned")

        response = {"message": "Role unassigned successfully", "code": "200"}
        transaction_log.complete_transaction(response, True)
        return JsonResponse(response)


    except:
        response = {"message": "Internal server error", "code": "500"}
        transaction_log.complete_transaction(response, False)
        return JsonResponse(response)


@csrf_exempt
def get_role_by_id(request):
    try:
        data = get_request_data(request)
        role_id = data.get('role_id')
        roles = RoleService().filter(uuid=role_id)
        role_list = list()
        for item in roles:
            data = {'uuid': item.uuid, 'name': item.name, 'description': item.description}
            role_list.append(data)
        return JsonResponse({"roles": role_list, "code": "200"})
    except:
        return JsonResponse({"message": "Internal server error", "code": "500"})


@csrf_exempt
def get_roles(request):
    try:
        data = get_request_data(request)
        event_id = data.get('event_id')
        active_state = StateService().get(name='active')
        event = EventService().get(uuid=event_id)
        roles = RoleService().filter(role_event=event, role_state=active_state)
        role_list = list()
        for item in roles:
            data = {'uuid': item.uuid, 'name': item.name, 'description': item.description}
            role_list.append(data)
        return JsonResponse({"roles": role_list, "code": "200"})
    except:
        return JsonResponse({"message": "Internal server error", "code": "500"})
