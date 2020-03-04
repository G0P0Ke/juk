from django.shortcuts import render


def _get_base_context(title):
    context = {
        'title': title,

    }
    return context


def index_view(request):
    context = _get_base_context('JUK')
    return render(request, 'pages/index.html', context)


def authorization_view(request):
    context = _get_base_context('authorization')
    if request.method == 'POST':
        pass
    context.update({
        'error': 'Неправильный логин или пароль',

    })
    return render(request, 'accounts/authorization/authorization_page.html', context)
