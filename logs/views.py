from base.backend.ServiceLayer import StateService
from base.models import State
from .backend.ServiceLayer import LogTypeService, LogService
from .models import LogType, Log


class TransactionLog(object):
    def __init__(self):
        self.log = None

    def start_transaction(self, user_id, log_type_name, request_data):
        state = StateService().get(name="ongoing")
        log_type = LogTypeService().get(name=log_type_name)
        self.log = LogService().create(
            user_id=user_id,
            log_type=log_type,
            request_data=request_data,
            state=state
        )

    def complete_transaction(self, response_data, is_successful=False):
        new_state = StateService().get(name="completed")
        LogService().update(self.log.uuid, is_successful=is_successful, response_data=response_data, state=new_state)

