from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('confirm-email/', views.confirm_email),
    path('forgot-password/', views.forgot_password),
    path('reset-password/', views.reset_password),
    path('change-credentials/', views.change_credentials),
]
