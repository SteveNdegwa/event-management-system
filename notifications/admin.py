from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'user_id', 'notification_state', 'date_created', 'date_modified')


# Register your models here.
admin.site.register(Notification, NotificationAdmin)
