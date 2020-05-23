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
    choices = [
        ('INTERESTING', 'interesting'),
        ('IMPORTANT', 'important'),
        ('URGENTLY', 'urgently')
    ]

    publicationTag = models.CharField(
        choices=choices,
        max_length=11,
        default='INTERESTING'
    )

    district = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE
    )
    publicationDate = models.DateTimeField(
        'date published'
    )
    publicationTitle = models.CharField(
        max_length=50
    )
    publicationText = models.TextField(
        max_length=5000
    )

