from django.http import JsonResponse
from base.backend.ServiceLayer import StateService
from core.backend.ServiceLayer import EventService
from invites.backend.ServiceLayer import InviteService
from logs.views import TransactionLog
from services.email_service import send_invitation_email
from services.request_processor import get_request_data


def invite_to_event(request):
    transaction_log = TransactionLog()
    try:
        # get request data
        data = get_request_data(request)
        user_id = data.get('user_id')
        event_id = data.get('event_id')
        target_email = data.get('email')

        # initialize transaction log
        transaction_log.start_transaction(user_id, 'invite', data)

        # get event instance
        event = EventService().get(uuid=event_id)

        # get ongoing state
        ongoing_state = StateService().get(name="ongoing")

        # save invite to database
        name = "Event Invite"
        description = f"You are invited to {event.name} - {event.description}"

        invite = InviteService().create(name=name, description=description, user_id=user_id, target_email=target_email, invite_event=event, invite_state=ongoing_state)

        # send invite
        send_invitation_email(user_id, target_email, name, description)

        # update state of invite
        completed_state = StateService().get(name='completed')
        InviteService().update(invite.uuid, invite_state=completed_state)

        response = {"message": "Invite sent successfully", "code": "200"}

        # complete transaction
        transaction_log.complete_transaction(response, True)

        return JsonResponse(response, status=200)

    except:
        response = {"message": "Internal server error", "code": "500"}
        transaction_log.complete_transaction(response, False)
        return JsonResponse(response, status=500)

