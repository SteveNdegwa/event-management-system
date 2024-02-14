from django.db import models
from base.models import GenericBaseModel, State
from core.models import Event


# Create your models here.

class Invite(GenericBaseModel):
    user_id = models.UUIDField()
    target_email = models.EmailField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)