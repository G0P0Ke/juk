"""
Используемые модули
"""
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm
from django.core.mail import send_mail
from .forms import FeedbackForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from tenant.models import Tenant, Company, Forum
from tenant.models import Manager, ManagerRequest
from tenant.forms import ManagerRequestForm, AppendCompany


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
    """
    Функция отображения страницы для обратной связи

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Отображене страницы
    """
    if request.method == "POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():
            subject = str(form.data['subject'])
            message = str(form.data['message'])
            user_mail = str(form.data['user_mail'])
            mail = 'juk_feedback_mail@mail.ru'
            subject_back = 'Отзывы о JUK'
            message_back = 'Ваш отзыв успешно отправлен'

            context = {
                'subject': subject,
                'message': message,
                'user_mail': user_mail,

            }

            message = 'Отправитель: ' + user_mail + '\n'\
                      + '\n' + message

            # TODO: оформление при помощи django forms
            # TODO: валидация входных параметров

            message = 'Отправитель: ' + user_mail + '\n' + '\n' + message

            # TODO: вынести отправку письма в отдельный субпроцесс (при помощи celery)
            send_mail(subject, message, mail,
                      [mail], fail_silently=False)

            send_mail(subject_back, message_back, mail,
                      [user_mail], fail_silently=False)

        else:
            pass

    return render(request, 'pages/feedback.html')


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
            elif request.POST.get("refused" + str(request_man.id)):
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
                new_company_forum = Forum.objects.create(company=c, categories="Объявления|Другое")
                new_company_forum.save()
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


