from django.contrib import admin
from logs.models import LogType, Log


class LogTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date_created', 'date_modified')


class LogAdmin(admin.ModelAdmin):
    list_display = ('log_type', 'user_id', 'request_data', 'response_data', 'state', 'is_successful', 'date_created', 'date_modified')


admin.site.register(LogType, LogTypeAdmin)
admin.site.register(Log, LogAdmin)
