from django.contrib import admin
from user_management.models import CachedUser


class CachedUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_superuser', 'is_active', 'is_staff', 'date_joined', 'last_login', 'date_created', 'date_modified')


# Register your models here.
admin.site.register(CachedUser, CachedUserAdmin)
