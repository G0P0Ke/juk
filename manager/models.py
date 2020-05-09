"""
Используемые модули
"""
from django.db import models
from django.contrib.auth.models import User
from tenant.models import Company


class News(models.Model):
    """
    Модель БД для новостей
    """
    companyName = models.CharField(max_length=50)
    publicationDate = models.DateTimeField('date published')
    publicationTitle = models.CharField(max_length=50)
    publicationText = models.TextField(max_length=5000)


class Manager(models.Model):
    """
    Модель БД для представителя УК
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
