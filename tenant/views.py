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

def helpdesk_view(request, id):
    context = {}
    helpdesk = HelpDesk.objects.get(pk=id)
    if request.method == 'POST':
        text = request.POST.get('message')
        # проверка на жителя
        message = HelpDeskSmartMessage.objects.create(text=text, helpdesk=helpdesk,
                                         creator="user", cr_date=datetime.now())
        # проверка на УК
        # message = Message.objects.create(text=text, helpdesk=helpdesk,
        #                                          creator="company", cr_date=datetime.now())
        message.save()
    messages = helpdesk.helpdesksmartmessage_set.all()
    messages = list(messages)
    messages.reverse()
    context.update({
        "user": request.user,
        "helpdesk": helpdesk,
        "smartmessages": messages,
    })
    return render(request, 'helpdesk.html', context)


def cr_helpdesk_view(request):
    context = {}
    if request.method == 'POST':
        theme = request.POST.get('theme')
        inn = int(request.POST.get("inn"))
        company = Company.objects.filter(inn=inn)[0]
        if request.user.tenant:
            helpdesk = HelpDesk(theme=theme, company=company,
                                user=request.user, cr_date=datetime.now())
            helpdesk.save()
        # if проверка на то что это представитель компании
        return redirect('/helpdesk/' + str(helpdesk.id))
    context.update({
        "user": request.user,
        "companies": Company.objects.all(),
        "is_tenant": True if request.user.tenant else False #-----------проверка на то является ли жителем------
    })
    return render(request, 'cr_helpdesk.html', context)


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

def discussion_view(request,id):
    discussion = Discussion.objects.get(id=id)
    comments = Comment.objects.filter(discussion = discussion)
    context = {
        "user": request.user,
        "comments":comments,
        "discussion":discussion,
    }
    if request.POST:
        text = request.POST.get("text")
        r_com = Comment(
            text=text,
            cr_date=datetime.now(),
            author=request.user,
            discussion = discussion
        )
        r_com.save()
        id = r_com.id
        return redirect('discussion', discussion.id)
    return render(request, 'discussion.html', context)

def thread(request,id,thread_id):
    thread = Comment.objects.get(id=thread_id)
    discussion = Discussion.objects.get(id=id)
    comments = Comment.objects.filter(thread=thread)
    context = {
        "user":request.user,
        "comments":comments,
        "thread":thread,
        "discussion":discussion
    }
    if request.POST:
        text = request.POST.get("text")
        r_com = Comment(
            text=text,
            cr_date=datetime.datetime.now(),
            author=request.user,
            discussion = discussion,
            thread = thread
        )
        r_com.save()
        id = r_com.id
        return redirect('thread', discussion.id, thread.id)
    return render(request, 'thread.html', context)

def category_view(request, id):
    context = {}
    forum = Forum.objects.get(pk=id)
    # request.user.id is not AnonymousUser:
    categories = []
    for c in forum.categories.split('|'):
        categories.append(Category(c, Discussion.objects.filter(category=c, forum=forum)))
    context.update({
        "user": request.user,
        "forum": forum,
        "categories": categories,
    })
    return render(request, 'category.html', context)


#@login_required
def cr_discussion_view(request, id):
    context = {}
    if request.method == 'POST':
        theme = request.POST.get('theme')
        category = request.POST.get('category')
        anonymous = request.POST.get('anonymous')
        if anonymous is None:
            anonymous = 0
        else:
            anonymous = 1
        discussion = Discussion(theme=theme, category=category, forum=Forum.objects.get(pk=id),
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

