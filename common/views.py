"""
Используемые модули
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm
from django.core.mail import send_mail
from .forms import FeedbackForm
from django.contrib.auth.models import AnonymousUser

from tenant.models import Tenant
from tenant.models import Manager

from .models import Feedback


def _get_base_context(title, sign_in_button=True):
    """
    Функция создания базового словаря

    :param title: Название страницы
    :param sign_in_button: Наличие кнопки авторизации
    :return: Базовый словарь
    """
    context = {
        'title': title,
        'if_sign_but': sign_in_button,

    }
    return context


def index_view(request):
    """
    Функция для отображения основной страницы

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Отображение страницы
    """
    context = _get_base_context('JUK')
    if request.user is not AnonymousUser:
        context.update({
            "is_tenant": hasattr(request.user, 'tenant'),
            "is_manager": hasattr(request.user, 'manager'),
        })
    return render(request, 'pages/index.html', context)


def login_view(request):
    """
    Функция отображения авторизации

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Возврат на основную страницу при успешной авторизации
    :return: Отображение страницы
    """
    context = _get_base_context('login', False)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['login'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if hasattr(user, 'tenant'):
                        return redirect('/tenant')
                    if hasattr(user, 'manager'):
                        return redirect('/manager')
                else:
                    context.update({
                        'error': 'Аккаунт отключён',
                    })
            else:
                context.update({
                    'error': 'Неправильный логин или пароль',
                })
    else:
        form = LoginForm()
    context.update({'form': form})
    return render(request, 'accounts/login/login_page.html', context)


def signup_view(request):
    """
    Функция отображения страницы регистрации

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Возвращение на главную страницу при успешной авториации
    :return: Отображение страницы
    """
    context = _get_base_context('sign up', False)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            print('save form')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            role = request.POST.get('role')
            if role == "tenant":
                tenant = Tenant.objects.create(user=user)
                tenant.save()
                return redirect('/tenant')
            elif role == "manager":
                manager = Manager.objects.create(user=user)
                manager.save()
                return redirect('/manager')
            
        else:
            context.update({
                'form': SignUpForm(request),
                'error': 'Форма не валидна',
            })
    else:
        context.update({
            'form': SignUpForm(),
        })
    return render(request, 'accounts/signup/signup_page.html', context)


def logout_view(request):
    """
    Функция выхода из аккаунта

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Переход на главную страницу
    """
    logout(request)
    return redirect('/')


def feedback(request):

    feedbacks = Feedback.objects.all()[::-1]

    context = {
        'feedbacks': feedbacks,
    }

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        context.update({
            'form': form,
        })
        if form.is_valid():
            post = form.save(commit=False)
            post.mail = 'juk_feedback_mail@mail.ru'
            post.title_back = 'Отзывы о JUK'
            post.text_back = 'Ваш отзыв успешно отправлен'
            post.finished = 0

            post.text = post.text

            post.save()
            return redirect('/common/feedback', context)
    else:
        form = FeedbackForm()
        context.update({
            'form': form,
        })
    return render(request, 'pages/feedback.html', context)
