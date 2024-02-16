from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_event),
    path("update/", views.update_event),
    path("delete/", views.delete_event),
    path("get/id/", views.get_event_by_id),
    path("get/", views.get_events),
    path("get/search/", views.search_events),
    path("invite/", views.invite),
    path("attend/", views.attend_event),
    path("roles/create/", views.create_role),
    path("roles/update/", views.update_role),
    path("roles/delete/", views.delete_role),
    path("roles/assign/", views.assign_role),
]
