from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    inn = models.CharField(max_length=10)


class House(models.Model):
    address = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # name inside
    house = models.ForeignKey(House, on_delete=models.CASCADE)
