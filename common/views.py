from django.shortcuts import render


def index_page(request):

    context = {

    }

    return render(request, 'pages/index.html', context)
