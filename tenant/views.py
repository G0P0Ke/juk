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
    Личный кабинет пользователя

    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри
    """
    if hasattr(request.user, 'tenant'):
        context = {
            "is_tenant": True,
            "user": request.user,
            "homeless": request.user.tenant.house is None,
            "house_confirmed": request.user.tenant.house_confirmed,
        }
    if hasattr(request.user, 'manager'):
        context = {
            "is_manager": True,
            "user": request.user,
            "companyless": request.user.manager.company is None,
        }
    #c = Company.objects.create(inn=666) #tmp
    #f2 = Forum.objects.create(company=c, categories="Объявления|Другое")#tmp
    #c.save()
    #f2.save()
    return render(request, 'pages/tenant/my_cabinet.html', context)


@login_required
def redact_profile_view(request):
    """
    Изменение профиля

    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри
    """
    user = request.user
    context = {
        "house_doesnt_exist": False,
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    }
    if request.method == 'POST':
        form = PhotoUpload(request.POST, request.FILES)
        if form.is_valid():
            photo = form.cleaned_data.get('photo')
            if hasattr(request.user, 'tenant'):
                user.tenant.photo = photo
                user.tenant.save(update_fields=['photo'])
            if hasattr(request.user, 'manager'):
                user.manager.photo = photo
                user.manager.save(update_fields=['photo'])
            context.update({
                "user": request.user,
                "form": form,
            })
            return render(request, 'pages/tenant/redact_profile.html', context)
    else:
        form = PhotoUpload()
    if request.method == 'POST' and hasattr(request.user, 'tenant'):
        username = request.POST.get('username')
        address = request.POST.get('address')
        user.username = username
        if request.user.tenant.house is None or address != request.user.tenant.house.address:
            user.tenant.house_confirmed = False
            if House.objects.filter(address=address).exists():
                user.tenant.house = House.objects.filter(address=address)[0]
            else:
                context.update({
                    "house_doesnt_exist": True,
                    'form': form,
                    "user": user,
                })
                return render(request, 'pages/tenant/redact_profile.html', context)
        user.tenant.flat = request.POST.get('flat')
        user.tenant.save()
        user.save()
        return redirect('/my_cabinet')
    if request.method == 'POST' and hasattr(request.user, 'manager'):
        username = request.POST.get('username')
        user.username = username
        request_form = ManagerRequestForm(request.POST)
        try:
            manager_request = ManagerRequest.objects.get(author_id=user.manager.user_id)
            if manager_request.status == 3:
                flag = 3
            elif manager_request.status == 2:
                flag = 2
            elif manager_request.status == 1:
                flag = 1
        except BaseException:
            flag = 0
        if request_form.is_valid():
            inn = request_form.cleaned_data.get('inn_company')
            try:
                get_Company = Company.objects.get(inn=inn)
                permission = 1
            except BaseException:
                permission = 0
            if permission:
                new_manager_request = ManagerRequest(author=user, inn_company=inn)
                new_manager_request.save()
                messages.success(request, 'Запрос на подключение отправлен')
            elif not permission:
                messages.info(request, 'Ваша УК не подключена к нашей системе')
            context.update({
                'request_form': request_form,
                'flag': flag,
            })
            return redirect(redact_profile_view)
    elif hasattr(request.user, 'manager'):
        request_form = ManagerRequestForm()
        try:
            manager_request = ManagerRequest.objects.get(author_id=user.manager.user_id)
            if manager_request.status == 3:
                flag = 3
            elif manager_request.status == 2:
                flag = 2
            elif manager_request.status == 1:
                flag = 1
        except BaseException:
            flag = 0
        context.update({
            'request_form': request_form,
            'flag': flag,
        })
    context.update({
        "user": user,
        'form': form,
        "companies": Company.objects.all(),
    })
    return render(request, 'pages/tenant/redact_profile.html', context)


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
    # request.user.id is not AnonymousUser:
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
    return render(request, 'pages/tenant/forum.html', context)


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
    return render(request, 'pages/tenant/category.html', context)


@login_required()
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
        return redirect('/forum/discussion/' + str(discussion.id))
    if hasattr(request.user, 'tenant'):
        photo_url = request.user.tenant.photo.url
        print(photo_url)
    if hasattr(request.user, 'manager'):
        photo_url = request.user.manager.photo.url
    comments = discussion.comment_set.all()
    comments = list(comments)
    #comments.reverse()
    context.update({
        "user": request.user,
        "discussion": discussion,
        "comments": comments,
        "photo_url": photo_url,
    })
    return render(request, 'pages/tenant/discussion.html', context)


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
    return render(request, 'pages/tenant/cr_discussion.html', context)


def thread(request, discussion_id, thread_id):
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
    comments = Comment.objects.filter(thread=thread)
    context = {
        "user": request.user,
        "comments": comments,
        "thread": thread,
        "discussion": discussion
    }
    if request.POST:
        text = request.POST.get("text")
        r_com = Comment(
            text=text,
            cr_date=datetime.datetime.now(),
            author=request.user,
            discussion=discussion,
            thread=current_thread
        )
        r_com.save()
        id = r_com.id
        return redirect('thread', discussion.id, thread.id)
    return render(request, 'pages/tenant/thread.html', context)


@login_required
def company_appeals_view(request):
    context = {}
    if hasattr(request.user, 'tenant'):
        my_appeals = request.user.tenant.appeal_set.all()
    if hasattr(request.user, 'manager'):
        my_appeals = request.user.manager.appeal_set.all()
    context.update({
        "my_appeals": my_appeals,
    })
    return render(request, 'pages/tenant/my_appeals.html', context)


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
    if hasattr(request.user, 'manager'):
        my_appeals = request.user.manager.appeal_set.all()
    context.update({
        "my_appeals": my_appeals,
    })
    return render(request, 'pages/tenant/my_appeals.html', context)


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
    return render(request, 'pages/tenant/appeal.html', context)


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
    return render(request, 'pages/tenant/cr_appeal.html', context)


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
            cr_date=datetime.datetime.now(),
        )
        task.save()
        return redirect('/vol/task/' + str(task.id))

    context.update({
        "user": request.user,
    })
    return render(request, 'pages/tenant/cr_task.html', context)


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
    }
    return render(request, 'pages/tenant/volunteer.html', context)


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
    }
    return render(request, 'pages/tenant/help.html', context)


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
    return render(request, 'pages/tenant/task.html', context)


@login_required
def test_view(request):
    context = {
        "user": request.user,
    }
    if request.method == 'POST':
        request.user.tenant.is_vol = True
        request.user.tenant.save()
    return render(request, 'pages/tenant/test.html', context)


@login_required
def main_page(request):
    #weather_api_key = "9894f93c-6bb8-45a2-95e2-6eee7ea9ab53"
    #Fedor key na zapas =)
    geocode_api_key = "ec60fb43-78d5-4e2e-af7c-da42c1300dbf"
    weather_api_key = "232ad7f1-a856-4ecd-92ad-30ea041f1b1e" #my key

    geocode = "Москва, Тверская улица, дом 7'"

    #будет для каждого индивидуально после подключения домов
    geo_url = urllib.parse.urlencode({ 'apikey' : geocode_api_key,
                                       'geocode' : geocode,
                                       'format' : 'json',
                                       'kind' : 'house',
                                       'results' : '1',
                                       })


    geo_url = "https://geocode-maps.yandex.ru/1.x/?"+geo_url
    geo_recv = requests.get(url=geo_url)
    first_json= json.loads(geo_recv.text)["response"]["GeoObjectCollection"]["featureMember"]
    point = first_json[0]["GeoObject"]["Point"]["pos"]
    point = point.split()
    
    lat = point[1]
    lon = point[0]

    forecast_url = urllib.parse.urlencode({ 'lat' : lat,
                                            'lon' : lon,
                                            'limit' : "1",
                                            'hours' : 'false',
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
    return render(request, 'main.html', context)


def my_pass_view(request):
    context = {
        'user': request.user,
        'my_pass': Pass.objects.filter(author=request.user, status='active'),
    }
    return render(request, 'pages/tenant/my_pass.html', context)


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
            return redirect('/tenant/pass/' + str(pas.id))
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
            return redirect('/tenant/pass/' + str(pas.id))
    return render(request, 'pages/tenant/cr_pass.html', context)


@login_required
def pass_view(request, pass_id):
    pas = Pass.objects.get(id=pass_id)
    tenant = 1
    if hasattr(request.user, 'manager'):
        tenant = 0
    link = "https://api.qrserver.com/v1/create-qr-code/?data=http://127.0.0.1:8000/tenant/pass/"\
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
        minutes = str(minutes) + ' минут'
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
    }
    if request.method == 'POST' or ti_del < datetime.timedelta(days=0):
        pas.status = 'complete'
        pas.save()
        return redirect('/')
    return render(request, 'pages/tenant/pass.html', context)


@login_required(login_url="/login")
def admin(request):
    user = request.user
    if hasattr(request.user, 'tenant'):
        if not user.tenant.is_admin:
            return HttpResponse("Nice try, bro", status=401)
    elif hasattr(request.user, 'manager'):
        if not user.manager.is_admin:
            return HttpResponse("Nice try, bro", status=401)
    manager_requests = ManagerRequest.objects.filter(status=3)
    context = {
        'requests': manager_requests,
    }
    if request.method == "POST":
        for request_man in manager_requests:
            if request.POST.get("agree"+str(request_man.id)):
                manager_id = request_man.author_id
                managers = Manager.objects.filter(user_id=manager_id)
                for manager in managers:
                    if manager.user_id == manager_id:
                        company = Company.objects.filter(inn=request_man.inn_company)
                        for comp in company:
                            if comp.inn == request_man.inn_company:
                                manager.company_id = comp.id
                                manager.save(update_fields=['company_id'])
                request_man.status = 1
                request_man.save()
            elif request.POST.get("refused"+str(request_man.id)):
                request_man.status = 2
                request_man.save()
        return redirect(admin)
    return render(request, 'admin/manager_requests.html', context)


def admin_create(request):
    user = request.user
    company = Company.objects.filter()
    context = {
        'company': company
    }
    if request.method == 'POST':
        form = AppendCompany(request.POST)
        if form.is_valid():
            inn = form.cleaned_data.get('inn_company')
            try:
                check_company = Company.objects.get(inn=inn)
                flag = 0
            except BaseException:
                flag = 1
            if flag:
                new_company = Company(inn=inn)
                new_company.save()
                messages.success(request, "УК добавлена")
            else:
                messages.info(request, 'УК с указанным ИНН уже существует')
            return redirect(admin_create)
    else:
        form = AppendCompany()
    context.update({
        'form': form
    })
    return render(request, 'admin/create_company.html', context)