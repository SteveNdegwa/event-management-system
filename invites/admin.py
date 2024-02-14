from django.contrib import admin
from invites.models import Invite


class InviteAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'target_email', 'event', 'state', 'date_created', 'date_modified')


# Register your models here.
admin.site.register(Invite, InviteAdmin)
