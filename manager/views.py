"""
Используемые модули
"""
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser

from .forms import CreateNewsForm
from .models import News
from tenant.models import Appeal, House, Forum, Tenant, Pass, Task


@login_required
def manager_main_page(request):
    amount_of_my_opened_tasks = 0
    for task in Task.objects.all():
        if hasattr(task.author, 'manager') and task.author.manager.company == request.user.manager.company:
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

    context = {
        "user": request.user,
        "companyless": request.user.manager.company is None,
    }
    # c = Company.objects.create(inn=666) #tmp
    # f2 = Forum.objects.create(company=c, categories="Объявления|Другое")#tmp
    # c.save()
    # f2.save()
    return render(request, 'pages/manager/my_cabinet.html', context)


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
                publicationDate=datetime.datetime.now(),
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
    context = {
        "user": request.user,
    }
    if request.method == 'POST':
        address = request.POST.get('address')
        house = House.objects.create(
            address=address,
            company=request.user.manager.company,
        )
        forum = Forum.objects.create(
            house=house,
            categories="Вода|Электричество|Субботник|Собрание ТСЖ|Другое",
        )
        house.save()
        forum.save()
        return redirect('/')
    return render(request, 'pages/manager/add_house.html', context)


class HouseContext:
    def __init__(self, house, unconfirmed_tenants):
        self.house = house
        self.unconfirmed_tenants = unconfirmed_tenants


@login_required
def tenant_confirming_view(request):
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
    context = {
        'company_name': request.user.manager.company.inn,
        'house_list': House.objects.filter(company=request.user.manager.company),
    }
    return render(request, 'pages/manager/manager_pass.html', context)


@login_required
def pass_list_view(request, house_id):
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

