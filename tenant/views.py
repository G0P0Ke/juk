"""Required modules"""
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import Company, House, Forum, Discussion, Comment, Tenant, Appeal, AppealMessage, Task, Pass
from .models import ManagerRequest, Manager
import datetime
import pytz
import requests
import urllib
import json
import os

from django.utils import timezone
from .forms import PhotoUpload, ManagerRequestForm, AppendCompany

from django.http import Http404


# from tenant.forms import EditProfileForm

# ЭТО ПРОФИЛЬ ОТ COMMON
# @login_required
# def profile(request):
#    context = {
#        'user': request.user,
#    }
#    if request.method == 'POST':
#        editprof = EditProfileForm(request.POST, instance=request.user)
#        if editprof.is_valid():
#            editprof.save()
#            context.update({
#                'editprof': editprof,
#             })
#         return redirect('/main/profile')
#     else:
#         editprof = EditProfileForm(instance=request.user)
#
#     context.update({
#         'editprof': editprof,
#     })
#
#     return render(request, 'pages/tenant/profile.html', context)


@login_required
def my_cabinet_view(request):
    """
    Личный кабинет жителя

    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри
    """
    if not hasattr(request.user, 'tenant'):
        return redirect('/')
    context = {
        "is_tenant": True,
        "user": request.user,
        "homeless": request.user.tenant.house is None,
        "house_confirmed": request.user.tenant.house_confirmed,
    }
    return render(request, 'pages/tenant/my_cabinet.html', context)


@login_required
def edit_profile_view(request):
    """
    Изменение профиля жильца

    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри
    """
    user = request.user
    if not hasattr(request.user, 'tenant'):
        return redirect('/')
    context = {
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    }
    if request.method == 'POST':
        form = PhotoUpload(request.POST, request.FILES)
        if form.is_valid():
            photo = form.cleaned_data.get('photo')
            user.tenant.photo = photo
            user.tenant.save(update_fields=['photo'])
            context.update({
                "user": user,
                "form": form,
            })
            return render(request, 'pages/tenant/edit_profile.html', context)
    else:
        form = PhotoUpload()
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        if request.user.tenant.house is None or address != request.user.tenant.house.address:
            user.tenant.house_confirmed = False
            if House.objects.filter(address=address).exists():
                user.tenant.house = House.objects.filter(address=address)[0]
                messages.success(request, 'Запрос на подключение отправлен')
            else:
                user.save()
                user.tenant.save()
                messages.info(request, 'Ваш дом не подключен к нашей системе')
                context.update({
                    'form': form,
                    "user": user,
                })
                return render(request, 'pages/tenant/edit_profile.html', context)
        user.tenant.flat = request.POST.get('flat')
        user.tenant.save()
        user.save()
        return redirect('/tenant/my_cabinet')
    context.update({
        "user": user,
        'form': form,
    })
    return render(request, 'pages/tenant/edit_profile.html', context)


class Category:
    """
    Служебный класс для передачи данных в context
    """

    def __init__(self, name, list_of_discussions, more):
        """
        :param name: название категории
        :param list_of_discussions: список обсуждений, относящийся к нему
        """
        self.name = name
        self.list_of_discussions = list_of_discussions
        self.more = more

    def name_pylint(self):
        """
        Функция, возвращающая имя. Нужна для pylint
        :return name: Имя
        """
        return self.name

    def list_of_discussions_pylint(self):
        """
            Функция, возвращающая список. Нужна для pylint
            :return name: список
        """
        return self.list_of_discussions()


def forum_view(request, forum_id):
    """
    Отображение форума с конкретным id

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param forum_id: primary key форума в БД
    :return: объект ответа сервера с HTML-кодом внутри
    """
    context = {}
    forum = Forum.objects.get(pk=forum_id)
    owner = ("house" if forum.house else "company")
    if owner == "house":
        context.update({"house": forum.house, })
    elif owner == "company":
        context.update({"company": forum.company, })
    categories = []
    for category in forum.categories.split('|'):
        discussions = list(Discussion.objects.filter(category=category, forum=forum))
        discussions.reverse()
        category = Category(category, discussions[:2], len(discussions) > 2)
        categories.append(category)
    context.update({
        "user": request.user,
        "forum": forum,
        "categories": categories,
        "house_forum": owner == "house",
        "company_forum": owner == "company",
    })
    if request.user is not AnonymousUser:
        context.update({
            "is_tenant": hasattr(request.user, 'tenant'),
            "is_manager": hasattr(request.user, 'manager'),
        })
    return render(request, 'pages/tenant/forums/forum.html', context)


def category_view(request, forum_id, category_name):
    """
    Отображение категорий, принадлежащих форуму с конкретным id

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param forum_id: primary key форума в БД
    :param category_name: название категории
    :return: объект ответа сервера с HTML-кодом внутри
    """
    context = {}
    forum = Forum.objects.get(pk=forum_id)
    discussions = list(Discussion.objects.filter(category=category_name, forum=forum))
    discussions.reverse()
    context.update({
        "user": request.user,
        "forum": forum,
        "discussions": discussions,
    })
    return render(request, 'pages/tenant/forums/category.html', context)


class CommentContext:
    """
    Служебный класс для передачи данных в context
    """

    def __init__(self, comment, answers_count):
        """
        :param comment: комметарий
        :param answers_count: количество ответов
        """
        self.comment = comment
        self.answers_count = answers_count


@login_required
def discussion_view(request, discussion_id):
    """
    Отображение обсуждения в форуме

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param discussion_id: primary key обсуждеиния в БД
    :return: объект ответа сервера с HTML-кодом внутри
    """
    context = {}
    discussion = Discussion.objects.get(pk=discussion_id)
    if request.method == 'POST':
        if request.user.id is AnonymousUser:
            return redirect('/login')
        text = request.POST.get('text')
        anon = bool(request.POST.get('anonymous'))
        comment = Comment.objects.create(
            text=text,
            discussion=discussion,
            author=request.user,
            cr_date=datetime.datetime.now(pytz.timezone("Europe/Moscow")),
            anon=anon,
        )
        comment.save()
        return redirect('/forum/discussion/'+str(discussion.id))
    comments = []
    for comment in discussion.comment_set.all():
        comments.append(CommentContext(comment, len(Comment.objects.filter(thread=comment))))
    # comments = list(comments)
    # comments.reverse()
    context.update({
        "user": request.user,
        "discussion": discussion,
        "comments": comments,
    })
    return render(request, 'pages/tenant/forums/discussion.html', context)


@login_required
def cr_discussion_view(request, forum_id):
    """
    Создание обсуждения

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param forum_id: primary key форума в БД
    :return: объект ответа сервера с HTML-кодом внутри в случае, если идёт GET-запрос на страницу
    :return: перенаправление на главную страницу в случае POST-запроса
    """
    context = {}
    if request.method == 'POST':
        theme = request.POST.get('theme')
        category = request.POST.get('category')
        description = request.POST.get('description')
        anonymous = request.POST.get('anonymous')
        anonymous = bool(anonymous)
        discussion = Discussion(
            theme=theme,
            category=category,
            forum=Forum.objects.get(pk=forum_id),
            description=description,
            author=request.user,
            cr_date=datetime.datetime.now(),
            anon_allowed=anonymous,
        )
        discussion.save()
        return redirect('/forum/discussion/' + str(discussion.id))
    forum = Forum.objects.get(pk=forum_id)
    categories = list(forum.categories.split('|'))
    context.update({
        "categories": categories,
        "forum": forum,
    })
    return render(request, 'pages/tenant/forums/cr_discussion.html', context)


def thread_view(request, discussion_id, thread_id):
    """
    Отображение треда

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param discussion_id: primary key дискуссии в БД
    :param thread_id: primary key треда в БД
    :return: перенаправление на страницу треда
    :return: рендер страницы треда
    """
    current_thread = Comment.objects.get(id=thread_id)
    discussion = Discussion.objects.get(id=discussion_id)
    comments = Comment.objects.filter(thread=current_thread)
    context = {
        "user": request.user,
        "comments": comments,
        "thread": current_thread,
        "discussion": discussion
    }
    if request.method == 'POST':
        text = request.POST.get("text")
        r_com = Comment(
            text=text,
            cr_date=datetime.datetime.now(),
            author=request.user,
            discussion=None,
            thread=current_thread
        )
        r_com.save()
        return redirect('thread', discussion.id, current_thread.id)
    return render(request, 'pages/tenant/forums/thread.html', context)


@login_required
def my_appeals_view(request):
    """
    Отображение моих обращений

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: отображзение страницы
    """
    context = {}
    if hasattr(request.user, 'tenant'):
        my_appeals = request.user.tenant.appeal_set.all()
        context.update({
            "is_tenant": True,
        })
    if hasattr(request.user, 'manager'):
        my_appeals = request.user.manager.appeal_set.all()
        context.update({
            "is_manager": True,
        })
    context.update({
        "my_appeals": my_appeals,
    })
    return render(request, 'pages/tenant/appeals/my_appeals.html', context)


class Message:
    """
    Служебный класс для передачи данных в context
    """
    def __init__(self, appealmessage, my_message):
        """
        :param appealmessage: сообщение
        :param my_message: моё или нет
        """
        self.appealmessage = appealmessage
        self.my_message = my_message


@login_required
def appeal_view(request, appeal_id):
    """
    Отображение обращения

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param appeal_id: id обращения
    :return: отображзение страницы
    """
    context = {}
    appeal = Appeal.objects.get(pk=appeal_id)
    if request.method == 'POST':
        text = request.POST.get('message')
        message = AppealMessage.objects.create(
            text=text,
            appeal=appeal,
            creator=request.user,
            cr_date=datetime.datetime.now(),
        )
        message.save()
        if hasattr(request.user, 'manager') and appeal.manager is None:
            appeal.manager = request.user.manager
            appeal.save()
        return redirect('/appeal/' + str(appeal.id))

    messages = []
    for appealmessage in appeal.appealmessage_set.all():
        messages.append(Message(appealmessage, appealmessage.creator == request.user))
    messages.reverse()
    context.update({
        "appeal": appeal,
        "appeal_messages": messages,
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
        "is_taken": appeal.manager is not None,
        "user": request.user,
    })
    return render(request, 'pages/tenant/appeals/appeal.html', context)


@login_required
def cr_appeal_view(request):
    context = {}
    if request.method == 'POST':
        theme = request.POST.get('theme')
        if hasattr(request.user, 'tenant'):
            appeal = Appeal(
                theme=theme,
                tenant=request.user.tenant,
                cr_date=datetime.datetime.now(),
            )
            appeal.save()
            message = request.POST.get('first_appeal_message')
            first_message = AppealMessage(
                appeal=appeal,
                text=message,
                cr_date=datetime.datetime.now(),
                creator=request.user,
            )
            first_message.save()
        if hasattr(request.user, 'manager'):
            username = request.POST.get('username')
            appeal = Appeal(
                theme=theme,
                manager=request.user.manager,
                tenant=User.objects.get(username=username).tenant,
                cr_date=datetime.datetime.now(),
            )
            appeal.save()
            message = request.POST.get('first_appeal_message')
            first_message = AppealMessage(
                appeal=appeal,
                text=message,
                cr_date=datetime.datetime.now(),
                creator=request.user,
            )
            first_message.save()
        return redirect('/appeal/' + str(appeal.id))

    if hasattr(request.user, 'manager'):
        tenants = []
        for tenant in Tenant.objects.all():
            if tenant.house.company == request.user.manager.company:
                tenants.append(tenant)
        context.update({"tenants": tenants})
    context.update({
        "user": request.user,
        "companies": Company.objects.all(),
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    })
    return render(request, 'pages/tenant/appeals/cr_appeal.html', context)


@login_required
def cr_task_view(request):
    """
    Создание задания для волонтёра

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    """
    context = {}
    if request.method == 'POST':
        description = request.POST.get('description')
        task = request.POST.get('task')
        task = Task(
            task=task,
            description=description,
            author=request.user,
            status='opened',
            cr_date=timezone.now(),
        )
        task.save()
        return redirect('/vol/task/' + str(task.id))

    context.update({
        "user": request.user,
    })
    return render(request, 'pages/tenant/volunteers/cr_task.html', context)


@login_required
def volunteer_view(request):
    opened_tasks = []
    taken_tasks = []
    closed_tasks = []
    if not hasattr(request.user, 'tenant'):
        return redirect('/')
    company = request.user.tenant.house.company
    for task in Task.objects.all():
        if (hasattr(task.author, 'manager') and task.author.manager.company == company or
                hasattr(task.author, 'tenant') and task.author.tenant.house.company == company) and task.status == "opened":
            opened_tasks.append(task)
        if task.volunteer == request.user.tenant and task.status == "taken":
            taken_tasks.append(task)
        if task.volunteer == request.user.tenant and task.status == "closed":
            closed_tasks.append(task)
    context = {
        "opened_tasks": opened_tasks,
        "taken_tasks": taken_tasks,
        "closed_tasks": closed_tasks,
        "company": company,
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    }
    return render(request, 'pages/tenant/volunteers/volunteer.html', context)


@login_required
def help_view(request):
    """
    Задания, созданные жителем

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    """
    user = request.user
    if hasattr(user, 'tenant'):
        opened_tasks = Task.objects.filter(author=request.user, status="opened",)
        taken_tasks = Task.objects.filter(author=request.user, status="taken", )
        closed_tasks = Task.objects.filter(author=request.user, status="closed", )
    if hasattr(user, 'manager'):
        opened_tasks = []
        taken_tasks = []
        closed_tasks = []
        for task in Task.objects.all():
            if hasattr(task.author, 'manager') and task.author.manager.company == user.manager.company:
                if task.status == "opened":
                    opened_tasks.append(task)
                if task.status == "taken":
                    taken_tasks.append(task)
                if task.status == "closed":
                    closed_tasks.append(task)
    context = {
        "opened_tasks": opened_tasks,
        "taken_tasks": taken_tasks,
        "closed_tasks": closed_tasks,
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    }
    return render(request, 'pages/tenant/volunteers/help.html', context)


@login_required
def task_view(request, id):
    task = Task.objects.get(pk=id)
    if hasattr(request.user, 'tenant'):
        my_task = request.user == task.author
    if hasattr(request.user, 'manager'):
        my_task = hasattr(task.author, 'manager') and request.user.manager.company == task.author.manager.company
    if request.method == 'POST' and hasattr(request.user, 'tenant'):
        status = request.POST.get('status')
        task.status = status
        if status == "taken":
            task.volunteer = request.user.tenant
        task.save()
    if request.method == 'POST' and hasattr(request.user, 'manager'):
        status = request.POST.get('status')
        task.status = status  # только closed
        task.save()
    context = {
        "user": request.user,
        "task": task,
        "my_task": my_task,
        "is_opened": task.status == "opened",
        "is_taken": task.status == "taken",
        "is_closed": task.status == "closed",
    }
    return render(request, 'pages/tenant/volunteers/task.html', context)


@login_required
def test_view(request):
    if not hasattr(request.user, 'tenant'):
        return redirect('/')
    if request.user.tenant.is_vol:
        return redirect('/')
    context = {
        "user": request.user,
    }
    if request.method == 'POST':
        if request.POST.get('1') == '3' and request.POST.get('2') == '1' and request.POST.get('3') == '1' and \
                request.POST.get('4') == '1' and request.POST.get('5') == '2':
            request.user.tenant.is_vol = 1
            request.user.tenant.save()
            return redirect('/tenant')
        else:
            request.user.tenant.test_date = timezone.now()
            request.user.tenant.save()
    if request.user.tenant.test_date is None:
        context.update({
            "date_ok": 1,
        })
    elif timezone.now() - request.user.tenant.test_date > datetime.timedelta(days=3):
        context.update({
            "date_ok": 1,
        })
    else:
        ti_del = datetime.timedelta(days=3) - (timezone.now() - request.user.tenant.test_date)
        hours = int(ti_del.seconds // 3600)
        if 10 <= hours <= 20:
            hours = str(hours) + ' часов'
        elif hours % 10 == 1:
            hours = str(hours) + ' час'
        elif hours % 10 == 2 or hours % 10 == 3 or hours % 10 == 4:
            hours = str(hours) + ' часа'
        else:
            hours = str(hours) + ' часов'
        minutes = (ti_del.seconds % 3600) // 60
        if 10 <= minutes <= 20:
            minutes = str(minutes) + ' минут'
        elif minutes % 10 == 1:
            minutes = str(minutes) + ' минута'
        elif minutes % 10 == 2 or minutes % 10 == 3 or minutes % 10 == 4:
            minutes = str(minutes) + ' минуты'
        else:
            minutes = str(minutes) + ' минут'
        context.update({
            "date_ok": 0,
            "days": ti_del.days,
            "hours": hours,
            "minutes": minutes,
        })
    return render(request, 'pages/tenant/volunteers/test.html', context)


@login_required
def tenant_main_page(request):
    if not hasattr(request.user, 'tenant'):
        return redirect('/')
    if request.user.tenant.house is None or not request.user.tenant.house_confirmed:
        context = {
            "homeless": request.user.tenant.house is None,
            "user": request.user,
            "house_confirmed": request.user.tenant.house_confirmed,
        }
        return render(request, 'pages/tenant/tenant.html', context)

    # погода ---------------------------------------------------------------------
    # weather_api_key = "9894f93c-6bb8-45a2-95e2-6eee7ea9ab53"
    # Fedor key na zapas =)
    geocode_api_key = "ec60fb43-78d5-4e2e-af7c-da42c1300dbf"
    weather_api_key = "232ad7f1-a856-4ecd-92ad-30ea041f1b1e"  # my key

    geocode = request.user.tenant.house.address

    # будет для каждого индивидуально после подключения домов
    geo_url = urllib.parse.urlencode({
        'apikey': geocode_api_key,
        'geocode': geocode,
        'format': 'json',
        'kind': 'house',
        'results': '1',
    })

    geo_url = "https://geocode-maps.yandex.ru/1.x/?"+geo_url
    geo_recv = requests.get(url=geo_url)
    first_json = json.loads(geo_recv.text)["response"]["GeoObjectCollection"]["featureMember"]
    point = first_json[0]["GeoObject"]["Point"]["pos"]
    point = point.split()
    
    lat = point[1]
    lon = point[0]

    forecast_url = urllib.parse.urlencode({
        'lat': lat,
        'lon': lon,
        'limit': "1",
        'hours': 'false',
    })

    forecast_url = "https://api.weather.yandex.ru/v1/forecast?" + forecast_url

    r = requests.get(url=forecast_url, headers={"X-Yandex-API-Key" : weather_api_key})
    forecasts = json.loads(r.text)["forecasts"][0]
    fore_night = forecasts["parts"]["night"]
    fore_morning = forecasts["parts"]["morning"]
    fore_day = forecasts["parts"]["day"]
    fore_evening = forecasts["parts"]["evening"]
    context = {
        "user": request.user,
        "night": fore_night["temp_avg"],
        "morning": fore_morning["temp_avg"],
        "day": fore_day["temp_avg"],
        "evening": fore_evening["temp_avg"],
        "night_icon": fore_night["icon"],
        "morning_icon": fore_morning["icon"],
        "day_icon": fore_day["icon"],
        "evening_icon": fore_evening["icon"],
    }
    # ----------------------------------------------------------------------------
    opened_tasks = Task.objects.filter(author=request.user, status="opened")
    context.update({
        "amount_of_my_opened_tasks": len(opened_tasks),
    })

    my_company = request.user.tenant.house.company
    amount_of_opened_tasks = 0
    amount_of_my_taken_tasks = 0
    for task in Task.objects.all():
        if hasattr(task.author, 'manager') and task.author.manager.company == my_company:
            if task.status == "opened":
                amount_of_opened_tasks += 1
            if task.status == "taken" and task.volunteer == request.user.tenant:
                amount_of_my_taken_tasks += 1
        if hasattr(task.author, 'tenant') and task.author.tenant.house.company == my_company:
            if task.status == "opened" and task.author != request.user:
                amount_of_opened_tasks += 1
            if task.status == "taken" and task.volunteer == request.user.tenant:
                amount_of_my_taken_tasks += 1
    context.update({
        "amount_of_opened_tasks": amount_of_opened_tasks,
        'amount_of_my_taken_tasks': amount_of_my_taken_tasks,
    })

    context.update({
        "house_forum_id": request.user.tenant.house.forum.id,
        "company_forum_id": request.user.tenant.house.company.forum.id,
    })

    context.update({
        "house_confirmed": request.user.tenant.house_confirmed,
    })
    return render(request, 'pages/tenant/tenant.html', context)


def my_pass_view(request):
    context = {
        'user': request.user,
        'my_pass': Pass.objects.filter(author=request.user, status='active'),
    }
    return render(request, 'pages/tenant/passes/my_pass.html', context)


@login_required
def cr_pass_view(request):
    context = {
        "user": request.user,
    }
    if request.method == 'POST':
        if request.POST.get('target') == 'person':
            pas = Pass(
                author=request.user,
                cr_date=timezone.now(),
                status='active',
                target=request.POST.get('target'),
                name=request.POST.get('name'),
                surname=request.POST.get('surname'),
                patronymic=request.POST.get('patronymic'),
                aim=request.POST.get('aim'),
            )
            pas.save()
            return redirect('/pass/' + str(pas.id))
        else:
            pas = Pass(
                author=request.user,
                cr_date=timezone.now(),
                status='active',
                target=request.POST.get('target'),
                model=request.POST.get('model'),
                color=request.POST.get('color'),
                number=request.POST.get('number'),
                aim=request.POST.get('aim'),
            )
            pas.save()
            return redirect('/pass/' + str(pas.id))
    return render(request, 'pages/tenant/passes/cr_pass.html', context)


@login_required
def pass_view(request, pass_id):
    pas = Pass.objects.get(id=pass_id)
    tenant = 1
    if hasattr(request.user, 'manager'):
        tenant = 0
    link = "https://api.qrserver.com/v1/create-qr-code/?data=http://127.0.0.1:8000/pass/"\
           + str(pass_id) + "&size=400x400"
    ti_del = datetime.timedelta(days=3) - (timezone.now() - pas.cr_date)
    hours = int(ti_del.seconds // 3600)
    if 10 <= hours <= 20:
        hours = str(hours)+' часов'
    elif hours % 10 == 1:
        hours = str(hours) + ' час'
    elif hours % 10 == 2 or hours % 10 == 3 or hours % 10 == 4:
        hours = str(hours) + ' часа'
    else:
        hours = str(hours) + ' часов'
    minutes = (ti_del.seconds % 3600) // 60
    if 10 <= minutes <= 20:
        minutes = str(minutes) + ' минут'
    elif minutes % 10 == 1:
        minutes = str(minutes) + ' минута'
    elif minutes % 10 == 2 or minutes % 10 == 3 or minutes % 10 == 4:
        minutes = str(minutes) + ' минуты'
    else:
        minutes = str(minutes) + ' минут'
    context = {
        'user': request.user,
        'pass': pas,
        'tenant': tenant,
        'link': link,
        'days': ti_del.days,
        'hours': hours,
        'minutes': minutes,
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    }
    if request.method == 'POST' or ti_del < datetime.timedelta(days=0):
        pas.status = 'complete'
        pas.save()
        if hasattr(request.user, 'tenant'):
            return redirect('/tenant')
        elif hasattr(request.user, 'manager'):
            return redirect('/manager')
    return render(request, 'pages/tenant/passes/pass.html', context)
