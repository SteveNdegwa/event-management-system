from base.models import BaseModel
from django.db import models


class CachedUser(BaseModel):
    user_id = models.UUIDField()
    username = models.CharField(max_length=255)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=False)
    date_joined = models.DateTimeField(editable=False)
    last_login = models.DateTimeField()
    role = models.CharField(max_length=255)