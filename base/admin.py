from django.contrib import admin
from .models import State


class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date_created', 'date_modified')


admin.site.register(State, StateAdmin)
