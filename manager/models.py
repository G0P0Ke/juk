"""
Используемые модули
"""
from django.db import models
from django.contrib.auth.models import User
from tenant.models import Company
from martor.models import MartorField


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

