"""
Используемые модули
"""
from django.db import models
from django.conf import settings


class Profile(models.Model):
    """
    Модель профиля
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # photo = models.ImageField(upload_to='users/', blank=True)
