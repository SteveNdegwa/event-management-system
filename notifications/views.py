from base.backend.ServiceLayer import StateService
from .backend.ServiceLayer import NotificationService


def create_notification(user_id, name, description):
    state = StateService().get(name="ongoing")
    notification_to_save = NotificationService().create(
        user_id=user_id,
        name=name,
        description=description,
        notification_state=state,
    )

    # send notification and if successful

    new_state = StateService().get(name="completed")
    NotificationService().update(notification_to_save.uuid, notification_state=new_state)

