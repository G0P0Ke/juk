from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    companyName = models.CharField(max_length=50)
    publicationDate = models.DateTimeField('date published')
    publicationTitle = models.CharField(max_length=50)
    publicationText = models.TextField(max_length=5000)


class Manager(models.Model):
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
