from base.backend.ServiceLayer import StateService
from services.email_service import send_notification_email
from user_management.backend.ServiceLayer import CachedUserService
from .backend.ServiceLayer import NotificationService


def create_notification(user_id, name, description):
    try:
        state = StateService().get(name="ongoing")
        notification_to_save = NotificationService().create(
            user_id=user_id,
            name=name,
            description=description,
            notification_state=state,
        )

        # send notification
        email = CachedUserService().get(user_id=user_id).email
        send_notification_email(user_id, email, name, description)

        new_state = StateService().get(name="completed")
        NotificationService().update(notification_to_save.uuid, notification_state=new_state)

    except:
        pass

