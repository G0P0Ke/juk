from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import datetime
from .forms import CreateNewsForm
from .models import News
from tenant.models import Appeal


def news_page(request):
    record = News.objects.all()
    context = {
        'user': request.user,
        'record': record,
    }
    return render(request, 'pages/manager/news/news.html', context)


@login_required
def create_news_page(request):
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
    context = {}
    return render(request, 'pages/manager/add_house.html', context)
