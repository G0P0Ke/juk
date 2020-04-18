from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    """
    Модель управляющей компании
    :param inn: инн УК
    """
    inn = models.IntegerField()


class House(models.Model):
    """
    Модель дома

    :param address: Адрес дома
    :param company: УК, которой принадлежит дом
    """
    address = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Tenant(models.Model):
    """
    Модель жильца

    :param user: Пользователь
    :param house: дом проживания пользователя
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # name inside
    house = models.ForeignKey(House, on_delete=models.CASCADE)


class Forum(models.Model):
    """
    Модель форума

    :param house: Дом, которому принадлежит форум (или)
    :param company: Компания, которой принадлежит форум (или)
    :param categories: Категории в форуме
    """
    house = models.OneToOneField(to=House, null=True, blank=True, on_delete=models.CASCADE)  # Дом форума
    company = models.OneToOneField(to=Company, null=True, blank=True, on_delete=models.CASCADE)
    categories = models.CharField(max_length=100, default="Вода|Электричество|Другое")


class Discussion(models.Model):
    """
    Модель обсуждения

    :param theme: Тема обсуждения
    :param category: Категория обсуждения
    :param discription: Описание обсуждения
    :param forum: Форум, которому принадлежит обсуждение
    :param author: Автор обсуждения
    :param cr_date: Дата создания обсуждения
    :param anon_allowed: Аноимное ли обсуждение
    """
    theme = models.TextField()  # Тема обсуждения
    category = models.TextField()  # Категория обсуждения
    description = models.TextField()  # Описание обсуждения
    forum = models.ForeignKey(to=Forum, on_delete=models.CASCADE)  # Родитель
    author = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)  # Автор
    cr_date = models.DateTimeField()  # Время создания обсуждения
    anon_allowed = models.BooleanField(default=False)  # можно ли анонимно комментировать


class Comment(models.Model):
    """
    Модель комментария

    :param text: Текст комментария
    :param discussion: Обсуждение, которому принадлежит комментарий
    :param author: Автор комментария
    :param cr_date: Дата создания комментария
    """
    text = models.TextField()  # Текст комментария
    discussion = models.ForeignKey(to=Discussion, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)  # Автор
    cr_date = models.DateTimeField()  # Время создания комментария


class HelpDesk(models.Model):
    theme = models.TextField()  # Тема обращения
    user = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)  # Пользователь
    company = models.ForeignKey(to=Company, null=True, on_delete=models.CASCADE)  # Компания
    cr_date = models.DateTimeField()  # Время создания обращения


class Message(models.Model):
    text = models.TextField()
    helpdesk = models.ForeignKey(to=HelpDesk, on_delete=models.CASCADE)
    creator = models.TextField(default="tenant")  # company или tenant
    cr_date = models.DateTimeField()  # Время создания сообщения
