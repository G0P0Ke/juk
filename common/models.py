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


class Feedback(models.Model):
    yourmail = models.EmailField(max_length=50)
    title = models.CharField(max_length=200)
    text = models.TextField()
    mail = models.EmailField(max_length=50)
    finished = models.BooleanField()
    title_back = models.CharField(max_length=50)
    text_back = models.CharField(max_length=50)