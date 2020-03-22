from django.shortcuts import render


def news_page(request):
    return render(request, 'manager/news.html', {})
