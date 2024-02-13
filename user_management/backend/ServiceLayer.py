from service_layer.ServiceLayer import ServiceLayer
from user_management.models import CachedUser


class CachedUserService(ServiceLayer):
    manager = CachedUser.objects