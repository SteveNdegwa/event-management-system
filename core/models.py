from base.models import BaseModel, GenericBaseModel, State
from django.db import models


class EventType(GenericBaseModel):
    event_type_state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Event(GenericBaseModel):
    creator_id = models.UUIDField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    venue = models.TextField()
    price = models.CharField(max_length=10)
    capacity = models.CharField(max_length=10)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    event_state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Role(GenericBaseModel):
    role_state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Attendee(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    gender = models.CharField(max_length=50)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    attendee_state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.uuid


class Ticket(BaseModel):
    ticket_attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    ticket_state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.uuid


class Notification(GenericBaseModel):
    user_id = models.UUIDField()
    notification_state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name






