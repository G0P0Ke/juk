from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # photo = models.ImageField(upload_to='users/', blank=True)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # photo = models.ImageField(upload_to='users/', blank=True)


class Company(models.Model):
    title = models.CharField(max_length=150)


class House(models.Model):
    address = models.CharField(max_length=150)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Manager(models.Model):
	user = models.OneToOneField(Profile, on_delete=models.CASCADE)
	company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Tennant(models.Model):
	user = models.OneToOneField(Profile, on_delete=models.CASCADE)
	house = models.ForeignKey(House, on_delete=models.CASCADE)





