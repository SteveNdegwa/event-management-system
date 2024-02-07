from django.db import models


# Create your models here.
class CachedUserRequest(models.Model):
    request_type = models.TextField()
    request_data = models.TextField()
    response_data = models.TextField()
    is_successful = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.request_type
