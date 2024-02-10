from django.db import models
from base.models import GenericBaseModel, State


class Notification(GenericBaseModel):
    user_id = models.UUIDField()
    notification_state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
