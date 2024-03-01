from django.contrib import admin
from .models import EventType, Event, Role, Attendee, Ticket


class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'event_type_state', 'date_created', 'date_modified')


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'creator_id', 'start', 'end', 'venue', 'price', 'capacity', 'image', 'event_type', 'event_state', 'date_created', 'date_modified')


class RoleAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'description', 'role_event', 'role_state', 'date_created', 'date_modified')


class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'event', 'role', 'attendee_state',  'date_created', 'date_modified')


class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_attendee', 'ticket_state', 'date_created', 'date_modified')


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Ticket, TicketAdmin)
