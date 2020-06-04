"""
Используемые модули
"""
from django.db import models
#from django.contrib.auth.models import User
from martor.models import MartorField
from tenant.models import Company


class News(models.Model):
    """
    Модель БД для новостей
    """
    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE,
    )
    publicationDate = models.DateTimeField(
        'date published'
    )
    publicationTitle = models.CharField(
        max_length=50
    )
    publicationText = MartorField()
    donation_on = models.BooleanField(
        default=False,
    )


class RegManager(models.Model):
    """
    Модель регистраци менеджера
    """
    fullName = models.CharField(max_length=200)
    userEmail = models.EmailField(max_length=50)
    ukEmail = models.EmailField(max_length=50)
    date = models.DateField()
    appointment = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=50)
    finished = models.BooleanField()
