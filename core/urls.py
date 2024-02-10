from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_event),
    path("update/<str:event_id>/", views.update_event),
    path("get/<str:event_id>/", views.get_event_by_id),
    path("get/", views.get_events),
    path("get/event-type/<str:event_type>/", views.get_events_by_type),
]
