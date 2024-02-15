from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('confirm-email/', views.confirm_email),
    path('forgot/', views.forgot_password),
    path('reset/', views.reset_password),
    path('change-credentials/', views.change_credentials),
]
