from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # photo = models.ImageField(upload_to='users/', blank=True)

class Feedback(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()