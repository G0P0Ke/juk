"""
Используемые модули
"""
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CreateNewsForm
from .models import News
from tenant.models import Appeal, House, Forum, Tenant


def news_page(request):
    """
    Функция для отображения страницы новостей

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: отображение страницы новостей
    """
    record = News.objects.all()
    context = {
        'user': request.user,
        'record': record,
    }
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
                companyName=request.user,
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
    return render(request, 'pages/manager/company_appeals.html', context)


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
        tenant_id = request.POST.get('confirming')
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
