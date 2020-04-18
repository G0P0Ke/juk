from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from .models import Company, House, Forum, Discussion, Comment, Tenant, HelpDesk, Message
from datetime import datetime
from django.contrib.auth.models import User


@login_required
def profile_view(request):
    """
    Профиль пользователя

    :param request: объект с деталями запроса.
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    """
    context = {
        "user": request.user,
    }
    #c = Company.objects.create(inn=666) #tmp
    #h = House.objects.create(address="Улица Крылатские Холмы 15к2", company=c)#tmp
    #f = Forum.objects.create(house=h, categories="Вода|Электричество|Субботник|Собрание ТСЖ|Другое")#tmp
    #f2 = Forum.objects.create(company=c, categories="Объявления|Другое")#tmp
    #request.user.tenant.house = h
    return render(request, 'profile.html', context)


@login_required
def redact_profile_view(request):
    context = {
        "house_doesnt_exist": False,
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        address = request.POST.get('address')
        request.user.username = username
        if House.objects.filter(address=address).exists():
            request.user.tenant.house = House.objects.filter(address=address)[0]
        else:
            context.update({
                "house_doesnt_exist": True,
                "user": request.user,
            })
            return render(request, 'redact_profile.html', context)

        request.user.save()
        return redirect('/profile')
    context.update({
        "user": request.user,
    })
    return render(request, 'redact_profile.html', context)


class Category:
    """
    Служебный класс для передачи данных в context
    """
    def __init__(self, name, list_of_discussions):
        """
        :param name: название категории
        :param list_of_discussions: список обсуждений, относящийся к нему
        """
        self.name = name
        self.list_of_discussions = list_of_discussions


def forum_view(request, id):
    """
    Отображение форума с конкретным id

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param id: primary key форума в БД
    :return: объект ответа сервера с HTML-кодом внутри
    """
    context = {}
    forum = Forum.objects.get(pk=id)
    owner = ("house" if Forum.objects.get(pk=id).house else "company")
    # request.user.id is not AnonymousUser:
    if owner == "house":
        context.update({"house": forum.house, })
    elif owner == "company":
        context.update({"company": forum.company, })
    categories = []
    for c in forum.categories.split('|'):
        categories.append(Category(c, Discussion.objects.filter(category=c, forum=forum)))
    context.update({
        "user": request.user,
        "forum": forum,
        "categories": categories,
        "house_forum": (True if owner == "house" else False),
        "company_forum": (True if owner == "company" else False),
    })
    return render(request, 'forum.html', context)


def discussion_view(request, id):
    """
    Отображение обсуждения в форуме

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param id: primary key обсуждеиния в БД
    :return: объект ответа сервера с HTML-кодом внутри
    """
    context = {}
    discussion = Discussion.objects.get(pk=id)
    if request.method == 'POST':
        if request.user.id is AnonymousUser:
            return redirect('/login')
        text = request.POST.get('comment')
        comment = Comment.objects.create(text=text, discussion=discussion,
                                         author=request.user, cr_date=datetime.now())
        comment.save()
    comments = discussion.comment_set.all()
    comments = list(comments)
    comments.reverse()
    context.update({
        "user": request.user,
        "discussion": discussion,
        "comments": comments
    })
    return render(request, 'discussion.html', context)


@login_required
def cr_discussion_view(request, id):
    """
    Создание обсуждения

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param id: primary key форума в БД
    :return: объект ответа сервера с HTML-кодом внутри в случае, если идёт GET-запрос на страницу
    :return: перенаправление на главную страницу в случае POST-запроса
    """
    context = {}
    if request.method == 'POST':
        theme = request.POST.get('theme')
        category = request.POST.get('category')
        description = request.POST.get('description')
        anonymous = request.POST.get('anonymous')
        anonymous = True if anonymous else False
        discussion = Discussion(theme=theme, category=category, forum=Forum.objects.get(pk=id), description=description,
                                author=request.user, cr_date=datetime.now(), anon_allowed=anonymous)
        discussion.save()
        return redirect('/forum/discussion/' + str(discussion.id))
    forum = Forum.objects.get(pk=id)
    categories = list(forum.categories.split('|'))
    context.update({
        "categories": categories,
        "forum": forum,
    })
    return render(request, 'cr_discussion.html', context)
