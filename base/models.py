import uuid

from django.db import models


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract: True


class GenericBaseModel(BaseModel):
    name = models.TextField()
    description = models.TextField()

    class Meta:
        abstract: True


class State(GenericBaseModel):
    def __str__(self):
        return self.name

