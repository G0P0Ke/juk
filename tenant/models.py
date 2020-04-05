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


class Discussion(models.Model):
    theme = models.TextField() # Тема обсуждения
    category = models.TextField() # Категория обсуждения
    description = models.TextField() # Содержание обсуждения
    forum = models.ForeignKey(to=User, on_delete=models.CASCADE) # Родитель
    author = models.ForeignKey(to=User, on_delete=models.CASCADE) # Автор
    cr_date = models.DateTimeField() # Время создания обсуждения


class Comment(models.Model):
    comment = models.TextField() # Текст комментария
    discussion = models.ForeignKey(to=Discussion, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE) # Автор
    cr_date = models.DateTimeField() # Время создания комментария


class Forum(models.Model):
    house = models.ForeignKey(to=House, on_delete=models.CASCADE) # Дом форума
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)
