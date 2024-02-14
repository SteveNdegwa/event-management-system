from invites.models import Invite
from services.ServiceLayer import ServiceLayer


class InviteService(ServiceLayer):
    manager = Invite.objects