from django.core.mail import send_mail

from juk.celery import app
from .models import RegManager


@app.task
def send_email(mail):
    title = 'Регистрация менеджера'
    text = 'Имя: ' + mail.fullName + '\n'
    text += 'Почта: ' + mail.userEmail + '\n'
    text += 'Почта УК: ' + mail.ukEmail + '\n'
    text += 'Должность: ' + mail.appointment + '\n'
    text += 'Номер телефона: ' + mail.phoneNumber
    juk_mail = 'juk_feedback_mail@mail.ru'
    title_back = 'Регистрация менеджера'
    text_back = 'Ваш запрос расматривается'

    send_mail(title, text, juk_mail, [juk_mail], fail_silently=False)
    send_mail(title_back, text_back, juk_mail, [mail.userEmail], fail_silently=False)

    #mail.save()
