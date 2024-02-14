from services.ServiceLayer import ServiceLayer
from user_management.models import CachedUser


class CachedUserService(ServiceLayer):
    manager = CachedUser.objects