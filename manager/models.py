from django.db import models
from django.contrib.auth.models import User
from tenant.models import Company


class News(models.Model):
    companyName = models.CharField(max_length=50)
    publicationDate = models.DateTimeField('date published')
    publicationTitle = models.CharField(max_length=50)
    publicationText = models.TextField(max_length=5000)


