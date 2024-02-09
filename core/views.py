import json
from django.http import JsonResponse

from .models import Event, Notification

def create_log(log_type, request_data, response_data, is_successful):
    try:
        log_type_uuid = LogType.objects.get(name=log_type)
        log = Log(log_type=log_type_uuid, request_data=request_data, response_data=response_data, status=status,
                  is_successful=is_successful)
        log.save()
    except:
        return JsonResponse({"message": "Internal server error"}, status=500)


def create_notification(user_id, name, description):
    try:
        notification = Notification(user_id=user_id, name=name, description=description)
        notification.save()
    except:
        return JsonResponse({"message": "Internal server error"}, status=500)


def create_event(request):
    try:
        user_id = request.COOKIES.get('user_id')
        data = json.loads(request.body)
        event = Event.objects.create(
            name=data.name,
            description=data.description,
            creator_id=user_id,
            start=data.start,
            end=data.end,
            venue=data.venue,
            capacity=data.capacity,
            event_type=data.event_type,
            event_state=data.event_state
        )
        create_notification(user_id, "Event created", f"You created an event: {data.name} - {data.description}")
        response = {"message": "Event created successfully", "status": "201"}
        create_log("create event", request.body, response, True)
        return JsonResponse(response, status=201)
    except:
        response = {"message": "Internal server error", "status": "500"}
        create_log("create event", request.body, response, False)
        return JsonResponse(response, status=500)


def update_event(request):
    try:
        user_id = request.user_id = request.COOKIES.get('user_id')
        data = json.loads(request.body)
        if user_id != data.creator_id:
            return JsonResponse({"message": "Not authorised to perform this operation"}, status=401)
        event = Event.objects.get(uuid=data.uuid)

    except:
        return JsonResponse({"message": "Internal server error"}, status=500)
