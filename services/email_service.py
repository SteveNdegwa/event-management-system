from django.core.mail import EmailMessage

from logs.views import TransactionLog


def email_sender(email, subject, message):
    mail_subject = subject
    message = message
    email = EmailMessage(
        mail_subject,
        message,
        to=[email]
    )
    email.send()


def send_notification_email(user_id, email, subject, message):
    trans_log = TransactionLog()
    try:
        trans_log.start_transaction(user_id, "receive_notification_email",
                                    {"user_id": user_id, "email": email, "subject": subject, "message": message})
        email_sender(email, subject, message)
        response = {"message": "Email sent successfully", "code": "200"}
        trans_log.complete_transaction(response, True)
    except:
        response = {"message": "Error sending email", "code": "500"}
        trans_log.complete_transaction(response, False)


def send_invitation_email(user_id, target_email, subject, message):
    trans_log = TransactionLog()
    try:
        trans_log.start_transaction(user_id, "send_invitation_email",
                                    {"user_id": user_id, "target_email": target_email, "subject": subject,
                                     "message": message})
        email_sender(target_email, subject, message)
        response = {"message": "Email sent successfully", "code": "200"}
        trans_log.complete_transaction(response, True)
    except:
        response = {"message": "Error sending email", "code": "500"}
        trans_log.complete_transaction(response, False)
