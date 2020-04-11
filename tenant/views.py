from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from .models import Company, House, Forum, Discussion, Comment
from .forms import DiscussionCreationForm
from datetime import datetime


def profile_view(request):
    context = {"user": request.user, }
    c = Company.objects.create(inn=1)#tmp
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
    form = DiscussionCreationForm()
    if request.method == 'POST':
        form = DiscussionCreationForm(request.POST)
        if form.is_valid():
            discussion = Discussion()
            discussion.author = request.user
            discussion.category = form.data['category']
            discussion.cr_date = datetime.now()
            discussion.description = form.data['description']
            discussion.theme = form.data['theme']
            discussion.forum = Forum.objects.get(pk=id)
            discussion.save()
            return redirect('/forum/discussion/' + str(discussion.id))
    context.update({
        "form": form,
    })
    return render(request, 'cr_discussion.html', context)
