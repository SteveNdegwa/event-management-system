from base.models import State
from service_layer.ServiceLayer import ServiceLayer


class StateService(ServiceLayer):
    manager = State.objects