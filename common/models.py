"""
Используемые модули
"""
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Модель профиля
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # photo = models.ImageField(upload_to='users/', blank=True)


class Admin(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    is_admin = models.BooleanField(
        default=False,
    )
    name = models.TextField(default=" ")  # имя менеджера
    surname = models.TextField(default=" ")  # фамилия менеджера