from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from .models import Company, House, Forum, Discussion, Comment
from datetime import datetime


def profile_view(request):
    context = {"user": request.user, }
    c = Company.objects.create(inn=1) #tmp
    h = House.objects.create(address="улица Пушкина дом Колотушкина", company=c)#tmp
    f = Forum.objects.create(house=h, categories="Вода|Электричество|Субботник|Собрание ТСЖ|Другое")#tmp
    return render(request, 'profile.html', context)


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
    context = {
        "user": request.user,
        "discussion": Discussion.objects.get(pk=id)
    }
    return render(request, 'discussion.html', context)


@login_required
def cr_discussion_view(request, id):
    context = {}
    if request.method == 'POST':
        theme = request.POST.get('theme')
        category = request.POST.get('category')
        description = request.POST.get('description')
        anonymous = request.POST.get('anonymous')
        if anonymous is None:
            anonymous = 0
        else:
            anonymous = 1
        discussion = Discussion(theme=theme, category=category, description=description,
                                forum=Forum.objects.get(pk=id), author=request.user,
                                cr_date=datetime.now(), anon_allowed=anonymous)
        discussion.save()
        return redirect('/forum/discussion/' + str(discussion.id))
    forum = Forum.objects.get(pk=id)
    categories = list(forum.categories.split('|'))
    context.update({
        "categories": categories,
        "forum": forum,
    })
    return render(request, 'cr_discussion.html', context)
