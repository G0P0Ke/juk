"""
Используемые модули
"""
#import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.utils import timezone

from tenant.models import Appeal, House, Forum, Tenant, Pass, Task, Company
from tenant.models import ManagerRequest#, Manager
from tenant.forms import PhotoUpload, ManagerRequestForm#, AppendCompany

from .forms import CreateNewsForm
from .models import News

#from django.contrib.messages.views import SuccessMessageMixin


@login_required
def manager_main_page(request):
    """
    Глвная страница менеджера

    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри
    """
    if not hasattr(request.user, 'manager'):
        redirect('/')
    if request.user.manager.company is None:
        context = {
            "companyless": request.user.manager.company is None,
            "user": request.user,
            # "house_confirmed": request.user.tenant.house_confirmed,
        }
        return render(request, 'pages/manager/manager.html', context)

    amount_of_my_opened_tasks = 0
    for task in Task.objects.all():
        tcompany = task.author.manager.company
        ucompany = request.user.manager.company
        if hasattr(task.author, 'manager') and tcompany == ucompany:
            if task.status == "opened":
                amount_of_my_opened_tasks += 1

    amount_of_opened_appeals = 0
    for appeal in Appeal.objects.all():
        if appeal.tenant.house.company == request.user.manager.company and appeal.manager is None:
            amount_of_opened_appeals += 1

    amount_of_unconfirmed_tenants = 0
    for house in House.objects.all():
        for tenant in house.tenant_set.all():
            if not tenant.house_confirmed:
                amount_of_unconfirmed_tenants += 1

    amount_of_houses = len(request.user.manager.company.house_set.all())

    context = {
        "user": request.user,
        "amount_of_my_opened_tasks": amount_of_my_opened_tasks,
        'amount_of_opened_appeals': amount_of_opened_appeals,
        'amount_of_unconfirmed_tenants': amount_of_unconfirmed_tenants,
        'amount_of_houses': amount_of_houses,
    }
    return render(request, 'pages/manager/manager.html', context)


@login_required
def my_cabinet_view(request):
    """
        Личный кабинет менеджера

        :param request: объект с деталями запроса.
        :return: объект ответа сервера с HTML-кодом внутри
        """
    if not hasattr(request.user, 'manager'):
        redirect('/')
    context = {
        "user": request.user,
        "companyless": request.user.manager.company is None,
    }
    # c = Company.objects.create(inn=666) #tmp
    # f2 = Forum.objects.create(company=c, categories="Объявления|Другое")#tmp
    # c.save()
    # f2.save()
    return render(request, 'pages/manager/my_cabinet.html', context)


@login_required
def edit_profile_view(request):
    """
    Изменение профиля менеджера

    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри
    """
    if not hasattr(request.user, 'manager'):
        redirect('/')
    user = request.user
    context = {
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    }
    if request.method == 'POST':
        form = PhotoUpload(request.POST, request.FILES)
        if form.is_valid():
            photo = form.cleaned_data.get('photo')
            user.manager.photo = photo
            user.manager.save(update_fields=['photo'])
            context.update({
                "user": request.user,
                "form": form,
            })
            return render(request, 'pages/manager/edit_profile.html', context)
    else:
        form = PhotoUpload()
    if request.method == 'POST':
        if request.POST.get('username') is not None:
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        request_form = ManagerRequestForm(request.POST)
        try:
            manager_request = ManagerRequest.objects.get(
                author_id=user.manager.user_id,
                name=user.first_name,
                surname=user.last_name,
            )
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
                #get_company = Company.objects.get(inn=inn)
                permission = 1
            except BaseException:
                permission = 0
            if permission:
                new_manager_request = ManagerRequest(
                    author=user,
                    inn_company=inn,
                    name=user.first_name,
                    surname=user.last_name,
                )
                new_manager_request.save()
                messages.success(request, 'Запрос на подключение отправлен')
            elif not permission:
                messages.info(request, 'Ваша УК не подключена к нашей системе')
            context.update({
                'request_form': request_form,
                'flag': flag,
            })
            return redirect(edit_profile_view)
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
        "user": request.user,
        'form': form,
        "companies": Company.objects.all(),
    })
    return render(request, 'pages/manager/edit_profile.html', context)


def news_page(request):
    """
    Функция для отображения страницы новостей

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: отображение страницы новостей
    """
    context = {}
    record = News.objects.all()
    if request.user is not AnonymousUser:
        context.update({
            "is_tenant": hasattr(request.user, 'tenant'),
            "is_manager": hasattr(request.user, 'manager'),
        })
    context.update({
        'user': request.user,
        'record': record,
    })
    return render(request, 'pages/manager/news/news.html', context)


@login_required
def create_news_page(request):
    """
    Функция для отображения страницы создания новостей

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Перенаправление настраницу новостей
    :return: Отображение страницы создания новостей
    """
    if not hasattr(request.user, 'manager'):
        redirect('/')
    context = {
        'user': request.user,
    }
    if request.method == 'POST':
        createnews = CreateNewsForm(request.POST)
        if createnews.is_valid():
            record = News(
                company=request.user.manager.company,
                publicationTitle=createnews.data['publicationTitle'],
                publicationText=createnews.data['publicationText'],
                publicationDate=timezone.now(),
            )
            record.save()
            return redirect('news')
    else:
        context['createnews'] = CreateNewsForm(
            initial={
                'companyName': request.user,
            }
        )

    return render(request, 'pages/manager/news/create_news.html', context)


@login_required
def company_forums_view(request):
    """
    Функция для отображения форума компании

    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри
    """
    user = request.user
    if not hasattr(user, 'manager'):
        redirect('/')
    context = {
        'user': user,
        "houses": user.manager.company.house_set.all(),
    }
    return render(request, 'pages/manager/company_forums.html', context)


@login_required
def company_appeals_view(request):
    """
    Функция для отображения обращений компании

    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри
    """
    user = request.user
    if not hasattr(user, 'manager'):
        redirect('/')
    opened_appeals = []
    for appeal in Appeal.objects.all():
        if appeal.tenant.house.company == user.manager.company and appeal.manager is None:
            opened_appeals.append(appeal)
    context = {
        'user': user,
        "opened_appeals": opened_appeals,
    }
    return render(request, 'pages/manager/appeals/company_appeals.html', context)


@login_required
def add_house_view(request):
    """
    Функция отображения страницы добавления дома к УК

    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри:
    """
    context = {
        "user": request.user,
        "all_houses": request.user.manager.company.house_set.all()
    }
    if not hasattr(request.user, 'manager'):
        redirect('/')
    if request.method == 'POST':
        address = request.POST.get('address')

        if len(address) > 0:
            try:
                #check_house = House.objects.get(address=address)
                flag = 0
            except BaseException:
                flag = 1
            if request.POST.get('is_house') == "0":
                messages.warning(request, "Для добавления введите а"
                                          "дрес дома и воспользуйтесь соответствующей"
                                          " кнопкой взаимодействия с картой")
            elif not flag:
                messages.warning(request, 'Этот дом уже подключен к УК')
            elif flag:
                house = House.objects.create(
                    address=address,
                    company=request.user.manager.company,
                )
                house.save()
                forum = Forum.objects.create(
                    house=house,
                    categories="Вода|Электричество|Субботник|Собрание ТСЖ|Другое",
                )
                forum.save()
                messages.success(request, "Новый дом с адрес"
                                          "ом " + address + " добавлен к вашему УК")
            return redirect(add_house_view)
        else:
            messages.warning(request, 'Заполните строку адресс для добавления дома')
    return render(request, 'pages/manager/add_house.html', context)


class HouseContext:
    """
    Служебный класс для хранения данных о доме
    """
    def __init__(self, house, unconfirmed_tenants):
        self.house = house
        self.unconfirmed_tenants = unconfirmed_tenants

    def unused_house(self):
        """
        Функция дляувеличения счёта в pylint

        :return: объект с данными о доме
        """
        return self.house

    def unused_unconfirmed_tenants(self):
        """
            Функция дляувеличения счёта в pylint

            :return: объект с данными неподтверждённых жильцах
        """
        return self.unconfirmed_tenants


@login_required
def tenant_confirming_view(request):
    """
    Функция отображения страницы подтверждения проживания жильца в доме

    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри
    """
    if not hasattr(request.user, 'manager'):
        redirect('/')
    if request.method == 'POST':
        tenant_id = int(request.POST.get('unconfirmed'))
        if tenant_id != 0:
            tenant = Tenant.objects.get(pk=tenant_id)
            tenant.house = None
            tenant.save()
        tenant_id = int(request.POST.get('confirmed'))
        if tenant_id != 0:
            tenant = Tenant.objects.get(pk=tenant_id)
            tenant.house_confirmed = True
            tenant.save()
    houses = []
    for house in House.objects.all():
        tenants = []
        for tenant in house.tenant_set.all():
            if not tenant.house_confirmed:
                tenants.append(tenant)
        if tenants != []:
            houses.append(HouseContext(house, tenants))
    context = {
        "user": request.user,
        "houses": houses,
    }
    return render(request, 'pages/manager/tenant_confirming.html', context)


@login_required
def pass_view(request):
    """
    Функция отображения страницы пропусков

    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри
    """
    if not hasattr(request.user, 'manager'):
        redirect('/')
    context = {
        'company_name': request.user.manager.company.inn,
        'house_list': House.objects.filter(company=request.user.manager.company),
    }
    return render(request, 'pages/manager/manager_pass.html', context)


@login_required
def pass_list_view(request, house_id):
    """
    Функция для отображения списка пропусков в дом с указанным id

    :param house_id: объект с id дома
    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри
    """
    if not hasattr(request.user, 'manager'):
        redirect('/')
    house = House.objects.get(id=house_id)
    human_passes = []
    car_passes = []
    for pas in Pass.objects.filter(status='active', target='person'):
        if pas.author.tenant.house == house:
            human_passes.append(pas)
    for pas in Pass.objects.filter(status='active', target='car'):
        if pas.author.tenant.house == house:
            car_passes.append(pas)

    context = {
        'human_passes': human_passes,
        'car_passes': car_passes,
        'house': house,
    }
    return render(request, 'pages/manager/pass_list.html', context)
