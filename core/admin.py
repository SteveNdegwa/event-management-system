from django.contrib import admin
from .models import EventType, Event, Role, Attendee, Ticket

admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(Role)
admin.site.register(Attendee)
admin.site.register(Ticket)
