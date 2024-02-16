from base.models import BaseModel, State
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
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(null=True)
    role = models.TextField()
    cached_user_state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username
