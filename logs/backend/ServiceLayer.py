from logs.models import Log, LogType
from service_layer.ServiceLayer import ServiceLayer


class LogTypeService(ServiceLayer):
    manager = LogType.objects


class LogService(ServiceLayer):
    manager = Log.objects
