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
    address = models.CharField(
        max_length=100
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )


class Tenant(models.Model):
    """
        Модель жильца

        :param user: Пользователь
        :param house: дом проживания пользователя
        """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE
    )


class Forum(models.Model):
    """
        Модель форума

        :param house: Дом, которому принадлежит форум (или)
        :param company: Компания, которой принадлежит форум (или)
        :param categories: Категории в форуме
        """
    house = models.OneToOneField(
        to=House,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    company = models.OneToOneField(
        to=Company,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    categories = models.CharField(
        max_length=100,
        default="Вода|Электричество|Другое"
    )


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
    theme = models.TextField()
    category = models.TextField()
    description = models.TextField()
    forum = models.ForeignKey(
        to=Forum, on_delete=models.CASCADE)
    author = models.ForeignKey(
        to=User,
        null=True,
        on_delete=models.CASCADE
    )
    cr_date = models.DateTimeField()
    anon_allowed = models.BooleanField(
        default=False
    )


class Comment(models.Model):
    """
        Модель комментария

        :param text: Текст комментария
        :param discussion: Обсуждение, которому принадлежит комментарий
        :param author: Автор комментария
        :param cr_date: Дата создания комментария
        """
    text = models.TextField()
    discussion = models.ForeignKey(
        to=Discussion,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    cr_date = models.DateTimeField()
    thread = models.ForeignKey(
        to='Comment',
        on_delete=models.CASCADE,
        default=None, null=True
    )


class Appeal(models.Model):
    """
        Модель обращения

        :param theme: Тема обращения
        :param user: житель обращения
        :param company: Компания обращения
        :param cr_date: Дата создания обращения
        """
    theme = models.TextField()
    user = models.ForeignKey(
        to=User,
        null=True,
        on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        to=Company,
        null=True,
        on_delete=models.CASCADE
    )
    cr_date = models.DateTimeField()


class AppealMessage(models.Model):
    """
        Модель обращения

        :param text: Текст сообщения
        :param appeal: обращение сообщения
        :param creator: Создатель ("company" или "tenant")
        :param cr_date: Дата создания сообщения
        """
    text = models.TextField()
    appeal = models.ForeignKey(
        to=Appeal,
        on_delete=models.CASCADE
    )
    creator = models.TextField(
        default="tenant"
    )
    cr_date = models.DateTimeField()


class Task(models.Model):
    """
    Модель задания для волонтёра

    :param description: Описание задания
    :param task: Сам текст задания
    :param author: Автор задания
    :param cr_date: Дата создания задания
    :param status: Статус выполнения задания
    :param address: Корпус, этаж и номер квартиры дающего задание
    """
    description = models.TextField(max_length=20)
    task = models.TextField(max_length=100)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    cr_date = models.DateTimeField(auto_now=True)
    status = models.TextField(max_length=20)
    address = models.TextField(max_length=20)
