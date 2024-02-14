from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_event),
    path("update/", views.update_event),
    path("get/id/", views.get_event_by_id),
    path("get/", views.get_events),
    path("get/search/", views.search_events),
    path("invite/", views.invite),
]
