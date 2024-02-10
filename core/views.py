import json
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from base.models import State
from .models import Event, EventType
from logs.views import TransactionLog
from notifications.views import create_notification


@csrf_exempt
def get_events(request):
    try:
        events = Event.objects.all()
        events_json = serializers.serialize('json', events)
        print(events_json)
        return JsonResponse({"events": events_json}, status=200)
    except:
        return JsonResponse({"message": "Internal server error", "status": "500"}, status=500)


@csrf_exempt
def get_event_by_id(request, event_id):
    try:
        event = Event.objects.get(uuid=event_id)
        print(event.uuid)
        return JsonResponse(event, status=200)
    except:
        return JsonResponse({"message": "Internal server error", "status": "500"}, status=500)


@csrf_exempt
def get_events_by_type(request, event_type):
    try:
        event_type = EventType.objects.get(name=event_type)
        events = Event.objects.filter(event_type=event_type)
        print(events[0].uuid)
        return JsonResponse(events, status=200)
    except:
        return JsonResponse({"message": "Internal server error", "status": "500"}, status=500)


@csrf_exempt
def create_event(request):
    transaction_log = TransactionLog()
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        transaction_log.start_transaction(user_id, 'create_event', data)
        state = State.objects.get(name='active')
        event_type = EventType.objects.get(name=data.get('event_type'))
        event = Event.objects.create(
            name=data.get('name'),
            description=data.get('description'),
            creator_id=user_id,
            start=data.get('start'),
            end=data.get('end'),
            venue=data.get('venue'),
            capacity=data.get('capacity'),
            price=data.get('price'),
            event_type=event_type,
            event_state=state
        )
        print(event.uuid)
        response = {"message": "Event created successfully", "status": "201"}
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
        response = {"message": "Internal server error", "status": "500"}
        transaction_log.complete_transaction(response, False)
        return JsonResponse(response, status=500)


@csrf_exempt
def update_event(request, event_id):
    transaction_log = TransactionLog()
    try:
        # user_id = request.COOKIES.get('user_id')
        data = json.loads(request.body)
        user_id = data.get('user_id')
        event = Event.objects.get(uuid=event_id)
        transaction_log.start_transaction(user_id, 'update_event', data)
        print(user_id, event.creator_id)
        if user_id != str(event.creator_id):
            response = {"message": "Not authorised to perform this operation", "code": "401"}
            transaction_log.complete_transaction(response, False)
            return JsonResponse(response, status=401)

        event_type = EventType.objects.get(name=data.get('event_type'))
        state = State.objects.get(name='active')

        event.name = data.get('name')
        event.description = data.get('description')
        event.start = data.get('start')
        event.end = data.get('end')
        event.venue = data.get('venue')
        event.capacity = data.get('capacity')
        event.price = data.get('price')
        event.event_type = event_type
        event.event_state = state
        event.save()

        response = {"message": "Event updated successfully", "status": "200"}
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


