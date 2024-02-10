from .models import Notification
from base.models import State


def create_notification(user_id, name, description):
    state = State.objects.get(name="ongoing")
    print(state)
    notification_to_save = Notification.objects.create(
        user_id=user_id,
        name=name,
        description=description,
        notification_state=state,
    )
    print(notification_to_save)

    # send notification and if successful

    new_state = State.objects.get(name="completed")
    saved_notification = Notification.objects.get(uuid=notification_to_save.uuid)
    saved_notification.notification_state = new_state
    saved_notification.save()
