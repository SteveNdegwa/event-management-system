from core.models import EventType, Event, Role, Attendee, Ticket
from services.ServiceLayer import ServiceLayer


class EventTypeService(ServiceLayer):
    manager = EventType.objects


class EventService(ServiceLayer):
    manager = Event.objects


class RoleService(ServiceLayer):
    manager = Role.objects


class AttendeeService(ServiceLayer):
    manager = Attendee.objects


class TicketService(ServiceLayer):
    manager = Ticket.objects