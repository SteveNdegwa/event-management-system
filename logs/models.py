from django.db import models
from base.models import GenericBaseModel, BaseModel, State


class LogType(GenericBaseModel):
    def __str__(self):
        return self.name


class Log(BaseModel):
    user_id = models.UUIDField()
    log_type = models.ForeignKey(LogType, on_delete=models.CASCADE)
    request_data = models.TextField()
    response_data = models.TextField(null=True, )
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return self.log_type.name

