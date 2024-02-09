from base.models import State
from models import LogType, Log


class TransactionLog(object):
    def __init__(self, log_type, request_data):
        state = State.objects.get(name="ongoing").uuid
        log_type_uuid = LogType.objects.get(name=log_type).uuid
        self.log = Log.objects.create(
            log_type=log_type_uuid,
            request_data=request_data,
            state=state
        )

    def complete_transaction(self, response_data, is_successful=False):
        state = State.objects.get(name="completed").uuid
        transaction_log = Log.objects.get(uuid=self.log.uuid)
        transaction_log.is_successful = is_successful
        transaction_log.response_data = response_data
        transaction_log.state = state
        transaction_log.save()
