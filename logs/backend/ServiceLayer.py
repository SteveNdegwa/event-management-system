from logs.models import Log, LogType
from services.ServiceLayer import ServiceLayer


class LogTypeService(ServiceLayer):
    manager = LogType.objects


class LogService(ServiceLayer):
    manager = Log.objects
