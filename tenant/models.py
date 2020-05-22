"""
Модули, используемые в моделях
"""
from django.db import models
from django.contrib.auth.models import User
from martor.models import MartorField


class Company(models.Model):
    """
    Модель управляющей компании

    :param inn: инн УК
    """
    inn = models.IntegerField()
    name = models.TextField(default=False)

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
        :param photo: фото жителя
        :param house: дом проживания пользователя
        :param is_vol: является ли житель волонтёром
        :param test_date: Время последнего прохождения (None eсли попыток не было)
        """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(
        upload_to='photo',
        blank=True,
        default='static/default.jpg',
    )
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    flat = models.TextField()
    is_vol = models.BooleanField(
        default=False,
    )
    test_date = models.DateTimeField(
        null=True,
        default=None,
    )
    house_confirmed = models.BooleanField(
        default=False,
    )
    is_admin = models.BooleanField(
        default=False,
    )


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
    photo = models.ImageField(
        upload_to='photo',
        blank=True,
        default='static/default.jpg',
    )
    is_admin = models.BooleanField(
        default=False,
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
    text = MartorField()
    discussion = models.ForeignKey(
        to=Discussion,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    cr_date = models.DateTimeField()
    #thread = models.ForeignKey(
    #    to='Comment',
    #    on_delete=models.CASCADE,
    #    default=None,
    #    null=True,
    #)
    anon = models.BooleanField(
        default=False
    )


class Appeal(models.Model):
    """
        Модель обращения

        :param theme: Тема обращения
        :param tenant: житель обращения
        :param manager: менеджер компании обращения
        :param cr_date: Дата создания обращения
        """
    theme = models.TextField()
    tenant = models.ForeignKey(
        to=Tenant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    manager = models.ForeignKey(
        to=Manager,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    cr_date = models.DateTimeField()


class AppealMessage(models.Model):
    """
        Модель обращения

        :param text: Текст сообщения
        :param appeal: обращение сообщения
        :param creator: Создатель
        :param cr_date: Дата создания сообщения
        """
    text = MartorField()
    appeal = models.ForeignKey(
        to=Appeal,
        on_delete=models.CASCADE,
    )
    creator = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    cr_date = models.DateTimeField()


class Task(models.Model):
    """
    Модель задания для волонтёра

    :param description: Описание задания
    :param task: Сам текст задания
    :param author: Автор задания (Житель)
    :param volunteer: Исполнитель задания (Пользователь)
    :param cr_date: Дата создания задания
    :param status: Статус выполнения задания ('opened' или 'taken' или 'closed')
    :param address: Корпус, этаж и номер квартиры дающего задание
    """
    description = models.TextField(
        max_length=20,
    )
    task = models.TextField(
        max_length=100,
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    volunteer = models.ForeignKey(
        to=Tenant,
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
    )
    cr_date = models.DateTimeField(
        auto_now=True
    )
    status = models.TextField(
        max_length=10
    )


class Pass(models.Model):
    """
    Модель БД для пропусков
    """
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    cr_date = models.DateTimeField()
    status = models.TextField()  # 'active' или 'complete'
    target = models.TextField()  # 'person' или 'car'
    name = models.TextField(
        null=True,
        blank=True,
    )  # Имя посетителя
    surname = models.TextField(
        null=True,
        blank=True,
    )  # Фамилия посетителя
    patronymic = models.TextField(
        null=True,
        blank=True,
    )  # Отчество посетителя
    model = models.TextField(
        null=True,
        blank=True,
    )  # Марка и модель машины
    color = models.TextField(
        null=True,
        blank=True,
    )  # Цвет машины
    number = models.TextField(
        null=True,
        blank=True,
    )  # Номер машины
    aim = models.TextField()  # Цель визита


class ManagerRequest(models.Model):
    """
    Модель запроса менеджера на подкдлючение к компании
    """
    statuses_requset = (
        (1, 'Accepted'),
        (2, 'Refused'),
        (3, 'Not considered')
    ) # статусы запроса на подключения
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )  # author
    name = models.TextField(
        default='Antosha'
    )  # имя менеджера
    surname = models.TextField(
        default='Andreev'
    )  # фамилия менеджера
    status = models.IntegerField(
        choices=statuses_requset,
        default=3
    )  # статус запроса на подключение
    inn_company = models.IntegerField()  # ИНН УК
