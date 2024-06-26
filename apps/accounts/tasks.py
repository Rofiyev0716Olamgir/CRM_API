import os
from django.core.mail import send_mail
from config.celery import app


@app.task(bind=True)
def send_mail_func(self, subject, message, recipient_list, *args, **kwargs):
    from_email = os.getenv('EMAIL_HOST_USER')
    send_mail(subject=subject,
              message=message,
              from_email=from_email,
              recipient_list=recipient_list,
              )
    return "Sent"