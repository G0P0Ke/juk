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


class Forum(models.Model):
    house = models.OneToOneField(to=House, null=True, on_delete=models.CASCADE)  # Дом форума
    company = models.OneToOneField(to=Company, null=True, on_delete=models.CASCADE)
    categories = models.CharField(max_length=100, default="Вода|Электричество|Другое")


class Discussion(models.Model):
    theme = models.TextField()  # Тема обсуждения
    category = models.TextField()  # Категория обсуждения
    description = models.TextField()  # Содержание обсуждения
    forum = models.ForeignKey(to=Forum, on_delete=models.CASCADE)  # Родитель
    author = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)  # Автор
    cr_date = models.DateTimeField()  # Время создания обсуждения
    anon_allowed = models.TextField(default=0)  # можно ли анонимно комментировать

class Comment(models.Model):
    text = models.TextField()  # Текст комментария
    discussion = models.ForeignKey(to=Discussion, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)  # Автор
    cr_date = models.DateTimeField()  # Время создания комментария
    thread = models.ForeignKey(to='Comment', on_delete=models.CASCADE, default=None, null=True)

