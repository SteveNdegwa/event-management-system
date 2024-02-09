from django.contrib import admin

from logs.models import LogType, Log

admin.site.register(LogType)
admin.site.register(Log)
