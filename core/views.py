from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from base.backend.ServiceLayer import StateService
from .backend.ServiceLayer import EventTypeService, EventService
from .backend.request_processor import get_request_data
from logs.views import TransactionLog
from notifications.views import create_notification


@csrf_exempt
def events_to_list(events):
    data = {}
    event_list = list()
    for item in events:
        data['name'] = item.name
        data['description'] = item.description
        data['creator_id'] = item.creator_id
        data['start'] = item.start
        data['end'] = item.end
        data['venue'] = item.venue
        data['price'] = item.price
        data['capacity'] = item.capacity
        data['event_type'] = item.event_type.name
        data['event_state'] = item.event_state.name
        event_list.append(data)
    return event_list


@csrf_exempt
def get_events(request):
    try:
        events = EventService().all()
        event_list = events_to_list(events)
        return JsonResponse({"events": event_list, "code": "200"}, status=200)
    except:
        return JsonResponse({"message": "Internal server error", "code": "500"}, status=500)


@csrf_exempt
def get_event_by_id(request):
    try:
        data = get_request_data(request)
        event_id = data.get('event_id')
        event = EventService().filter(uuid=event_id)
        event_list = events_to_list(event)
        return JsonResponse({"events": event_list, "code": "200"}, status=200)
    except:
        return JsonResponse({"message": "Internal server error", "code": "500"}, status=500)


@csrf_exempt
def search_events(request):
    try:
        data = get_request_data(request)
        search = data.get('search')

        event_type = EventTypeService().get(name=search)
        event_state = StateService().get(name=search)

        events = EventService().filter(name=search) | EventService().filter(description=search) | EventService().filter(
            creator_id=search) | EventService().filter(start=search) | EventService().filter(
            end=search) | EventService().filter(venue=search) | EventService().filter(
            price=search) | EventService().filter(capacity=search) | EventService().filter(
            event_state=event_state) | EventService().filter(event_type=event_type)

        event_list = events_to_list(events)
        return JsonResponse({"events": event_list, "code": "200"}, status=200)
    except:
        return JsonResponse({"message": "Internal server error", "code": "500"}, status=500)


@csrf_exempt
def create_event(request):
    transaction_log = TransactionLog()
    try:
        data = get_request_data(request)
        user_id = data.get('user_id')

        transaction_log.start_transaction(user_id, 'create_event', data)

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
            event_type=event_type,
            event_state=event_state,
        )
        print(event.uuid)
        response = {"message": "Event created successfully", "code": "201"}
        transaction_log.complete_transaction(response, True)

        try:
            create_notification(user_id, "Event created",
                                f"You created an event: {data.get('name')} - {data.get('description')}")
            print("notification created")
        except:
            print("error creating notification")
            pass

        return JsonResponse(response, status=201)
    except:
        response = {"message": "Internal server error", "code": "500"}
        transaction_log.complete_transaction(response, False)
        return JsonResponse(response, status=500)


@csrf_exempt
def update_event(request):
    transaction_log = TransactionLog()
    try:
        # user_id = request.COOKIES.get('user_id')
        data = get_request_data(request)
        event_id = data.get('event_id')
        user_id = data.get('user_id')

        event = EventService().get(uuid=event_id)

        transaction_log.start_transaction(user_id, 'update_event', data)

        if user_id != str(event.creator_id):
            response = {"message": "Not authorised to perform this operation", "code": "403"}
            transaction_log.complete_transaction(response, False)
            return JsonResponse(response, status=403)

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
            event_type=event_type,
            event_state=state,
        )

        response = {"message": "Event updated successfully", "code": "200"}
        transaction_log.complete_transaction(response, True)

        try:
            create_notification(user_id, "Event Updated",
                                f"Event: '{data.get('name')}' - '{data.get('description')}' updated successfully")
            print("notification created")
        except:
            print("error creating notification")
            pass

        return JsonResponse(response, status=200)


    except:
        response = {"message": "Internal server error", "code": "500"}
        transaction_log.complete_transaction(response, False)
        return JsonResponse(response, status=500)
