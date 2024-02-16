from base.models import State
from services.ServiceLayer import ServiceLayer


class StateService(ServiceLayer):
    manager = State.objects