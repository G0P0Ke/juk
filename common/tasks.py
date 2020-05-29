from django.core.mail import send_mail

from juk.celery import app
from .models import Feedback


@app.task
def send_email(mail):
    send_mail(mail.title, mail.text, mail.mail, [mail.mail], fail_silently=False)
    send_mail(mail.title_back, mail.text_back, mail.mail, [mail.yourmail], fail_silently=False)
    mail.finished = 1
    #mail.save()
