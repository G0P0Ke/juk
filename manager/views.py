from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import datetime
from .forms import CreateNewsForm
from .models import News


def news_page(request):
    record = News.objects.all()
    context = {
        'user': request.user,
        'record': record,
    }
    return render(request, 'manager/news.html', context)


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

    return render(request, 'manager/create_news.html', context)
