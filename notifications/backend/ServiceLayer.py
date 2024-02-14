from notifications.models import Notification
from services.ServiceLayer import ServiceLayer


class NotificationService(ServiceLayer):
    manager = Notification.objects