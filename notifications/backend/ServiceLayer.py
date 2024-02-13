from notifications.models import Notification
from service_layer.ServiceLayer import ServiceLayer


class NotificationService(ServiceLayer):
    manager = Notification.objects