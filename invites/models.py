from django.db import models
from base.models import GenericBaseModel, State
from core.models import Event


# Create your models here.

class Invite(GenericBaseModel):
    user_id = models.UUIDField()
    target_email = models.EmailField()
    invite_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    invite_state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.description}"
