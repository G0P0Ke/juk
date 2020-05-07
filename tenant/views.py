from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User

from .models import Company, House, Forum, Discussion, Comment, Tenant, Appeal, AppealMessage, Task
import datetime


from .forms import PhotoUpload

from django.http import Http404


# from tenant.forms import EditProfileForm

# ЭТО ПРОФИЛЬ ОТ COMMON
# @login_required
# def profile(request):
#    context = {
#        'user': request.user,
#    }
#    if request.method == 'POST':
#        editprof = EditProfileForm(request.POST, instance=request.user)
#        if editprof.is_valid():
#            editprof.save()
#            context.update({
#                'editprof': editprof,
#             })
#         return redirect('/main/profile')
#     else:
#         editprof = EditProfileForm(instance=request.user)
#
#     context.update({
#         'editprof': editprof,
#     })
#
#     return render(request, 'pages/tenant/profile.html', context)


@login_required
def my_cabinet_view(request):
    """
    Личный кабинет пользователя

    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри
    """
    if hasattr(request.user, 'tenant'):
        context = {
            "is_tenant": True,
            "user": request.user,
            "homeless": request.user.tenant.house is None,
        }
    if hasattr(request.user, 'manager'):
        context = {
            "is_manager": True,
            "user": request.user,
            "companyless": request.user.manager.company is None,
        }
        # c = Company.objects.create(inn=666) #tmp
        # h = House.objects.create(address="Улица Крылатские Холмы 15к2", company=c)#tmp
        # t = Tenant.objects.create(user=request.user, house=h)  # tmp
        # f = Forum.objects.create(house=h, categories="Вода|Электричество|Субботник|Собрание ТСЖ|Другое")#tmp
        # f2 = Forum.objects.create(company=c, categories="Объявления|Другое")#tmp
    return render(request, 'pages/tenant/my_cabinet.html', context)


@login_required
def redact_profile_view(request):
    user = request.user
    context = {
        "house_doesnt_exist": False,
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    }
    if request.method == 'POST':
        form = PhotoUpload(request.POST, request.FILES)
        if form.is_valid():
            photo = form.cleaned_data.get('photo')
            if hasattr(request.user, 'tenant'):
                user.tenant.photo = photo
                user.tenant.save(update_fields=['photo'])
            if hasattr(request.user, 'manager'):
                user.manager.photo = photo
                user.manager.save(update_fields=['photo'])
            context.update({
                "user": request.user,
                "form": form,
            })
            return render(request, 'pages/tenant/redact_profile.html', context)
    else:
        form = PhotoUpload()
    if request.method == 'POST' and hasattr(request.user, 'tenant'):
        username = request.POST.get('username')
        address = request.POST.get('address')
        user.username = username
        if House.objects.filter(address=address).exists():
            user.tenant.house = House.objects.filter(address=address)[0]
        else:
            context.update({
                "house_doesnt_exist": True,
                'form': form,
                "user": user,
            })
            return render(request, 'pages/tenant/redact_profile.html', context)
        user.tenant.save()
        user.save()
        return redirect('/my_cabinet')
    if request.method == 'POST' and hasattr(request.user, 'manager'):
        username = request.POST.get('username')
        company_inn = request.POST.get('company_inn')
        user.username = username
        user.manager.company = Company.objects.filter(inn=company_inn)[0]
        user.manager.save()
        user.save()
        return redirect('/my_cabinet')

    context.update({
        "user": user,
        'form': form,
        "companies": Company.objects.all(),
    })
    return render(request, 'pages/tenant/redact_profile.html', context)


class Category:
    """
    Служебный класс для передачи данных в context
    """
    def __init__(self, name, list_of_discussions, more):
        """
        :param name: название категории
        :param list_of_discussions: список обсуждений, относящийся к нему
        """
        self.name = name
        self.list_of_discussions = list_of_discussions
        self.more = more


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
    owner = ("house" if forum.house else "company")
    # request.user.id is not AnonymousUser:
    if owner == "house":
        context.update({"house": forum.house, })
    elif owner == "company":
        context.update({"company": forum.company, })
    categories = []
    for c in forum.categories.split('|'):
        discussions = list(Discussion.objects.filter(category=c, forum=forum))
        discussions.reverse()
        category = Category(c, discussions[:2], len(discussions) > 2)
        categories.append(category)
    context.update({
        "user": request.user,
        "forum": forum,
        "categories": categories,
        "house_forum": (True if owner == "house" else False),
        "company_forum": (True if owner == "company" else False),
    })
    return render(request, 'pages/tenant/forum.html', context)


def category_view(request, id, name):
    context = {}
    forum = Forum.objects.get(pk=id)
    discussions = list(Discussion.objects.filter(category=name, forum=forum))
    discussions.reverse()
    context.update({
        "user": request.user,
        "forum": forum,
        "discussions": discussions,
    })
    return render(request, 'pages/tenant/category.html', context)


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
        text = request.POST.get('text')
        comment = Comment.objects.create(
            text=text,
            discussion=discussion,
            author=request.user,
            cr_date=datetime.datetime.now(),
        )
        comment.save()
    comments = discussion.comment_set.all()
    comments = list(comments)
    comments.reverse()
    context.update({
        "user": request.user,
        "discussion": discussion,
        "comments": comments,
    })
    return render(request, 'pages/tenant/discussion.html', context)


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
        discussion = Discussion(
            theme=theme,
            category=category,
            forum=Forum.objects.get(pk=id),
            description=description,
            author=request.user,
            cr_date=datetime.datetime.now(),
            anon_allowed=anonymous,
        )
        discussion.save()
        return redirect('/forum/discussion/' + str(discussion.id))
    forum = Forum.objects.get(pk=id)
    categories = list(forum.categories.split('|'))
    context.update({
        "categories": categories,
        "forum": forum,
    })
    return render(request, 'pages/tenant/cr_discussion.html', context)


def thread(request, id, thread_id):
    thread = Comment.objects.get(id=thread_id)
    discussion = Discussion.objects.get(id=id)
    comments = Comment.objects.filter(thread=thread)
    context = {
        "user": request.user,
        "comments": comments,
        "thread": thread,
        "discussion": discussion
    }
    if request.POST:
        text = request.POST.get("text")
        r_com = Comment(
            text=text,
            cr_date=datetime.datetime.now(),
            author=request.user,
            discussion=discussion,
            thread=thread
        )
        r_com.save()
        id = r_com.id
        return redirect('thread', discussion.id, thread.id)
    return render(request, 'pages/tenant/thread.html', context)


@login_required
def my_appeals_view(request):
    context = {}
    user_appeals = request.user.appeal_set.all()
    context.update({
        "user_appeals": user_appeals,

    })
    return render(request, 'pages/tenant/my_appeals.html', context)


@login_required
def appeal_view(request, id):
    context = {}
    appeal = Appeal.objects.get(pk=id)
    if request.method == 'POST':
        text = request.POST.get('message')
        # проверка на жителя
        message = AppealMessage.objects.create(
            text=text,
            appeal=appeal,
            creator="tenant",
            cr_date=datetime.datetime.now()
        )
        message.save()
        return redirect('/appeal/' + str(appeal.id))
    messages = appeal.appealmessage_set.all()
    messages = list(messages)
    messages.reverse()
    context.update({
        "user": request.user,
        "appeal": appeal,
        "appeal_messages": messages,
    })
    return render(request, 'pages/tenant/appeal.html', context)


@login_required
def cr_appeal_view(request):
    context = {}
    if request.method == 'POST':
        theme = request.POST.get('theme')
        if request.user.tenant:
            company = request.user.tenant.house.company
            appeal = Appeal(
                theme=theme,
                company=company,
                user=request.user,
                cr_date=datetime.datetime.now(),
            )
            appeal.save()
            message = request.POST.get('first_appeal_message')
            first_message = AppealMessage(
                appeal=appeal,
                text=message,
                cr_date=datetime.datetime.now(),
                creator="tenant"
            )
            first_message.save()
        # if проверка на то что это представитель компании
        #
        #
        return redirect('/appeal/' + str(appeal.id))
    context.update({
        "user": request.user,
        "companies": Company.objects.all(),
        "is_tenant": True if request.user.tenant else False  # -----------проверка на то является ли жителем------
    })
    return render(request, 'pages/tenant/cr_appeal.html', context)


@login_required
def cr_task_view(request):
    """
    Создание задания для волонтёра

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    """
    context = {}
    if request.method == 'POST':
        description = request.POST.get('description')
        task = request.POST.get('task')
        task = Task(
            task=task,
            description=description,
            author=request.user,
            status='opened',
            cr_date=datetime.datetime.now(),
        )
        task.save()
        return redirect('/vol/task/' + str(task.id))

    context.update({
        "user": request.user,
    })
    return render(request, 'pages/tenant/cr_task.html', context)


@login_required
def volunteer_view(request):
    opened_tasks = []
    taken_tasks = []
    closed_tasks = []
    if hasattr(request.user, 'tenant'):
        company = request.user.tenant.house.company
    if hasattr(request.user, 'manager'):
        company = request.user.manager.company
    for task in Task.objects.all():
        if task.author.house.company == company and task.status == "opened":
            opened_tasks.append(task)
        if task.volunteer == request.user and task.status == "taken":
            taken_tasks.append(task)
        if task.volunteer == request.user and task.status == "closed":
            closed_tasks.append(task)
    context = {
        "opened_tasks": opened_tasks,
        "taken_tasks": taken_tasks,
        "closed_tasks": closed_tasks,
        "company": company,
    }
    return render(request, 'pages/tenant/volunteer.html', context)


@login_required
def help_view(request):
    """
    Задания, созданные жителем

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    """
    user = request.user
    if hasattr(user, 'tenant'):
        tasks = Task.objects.filter(author=request.user)
    if hasattr(user, 'manager'):
        tasks = []
        for task in Task.objects.all():
            if task.author.tenant.house.company == user.manager.company:
                tasks.append(task)
    context = {
        "tasks": tasks,
    }
    return render(request, 'pages/tenant/help.html', context)


def task_view(request, id):
    task = Task.objects.get(pk=id)
    if hasattr(request.user, 'tenant'):
        my_task = (True if request.user.tenant == task.author else False)
    if hasattr(request.user, 'manager'):
        my_task = True
    if request.method == 'POST' and hasattr(request.user, 'tenant'):
        status = request.POST.get('status')
        task.status = status
        if status == "taken":
            task.volunteer = request.user.tenant
        task.save()
    if request.method == 'POST' and hasattr(request.user, 'manager'):
        status = request.POST.get('status')
        task.status = status  # только closed
        task.save()
    context = {
        "user": request.user,
        "task": task,
        "my_task": my_task,
        "is_opened": True if task.status == "opened" else False,
        "is_taken": True if task.status == "taken" else False,
        "is_closed": True if task.status == "closed" else False,
    }
    return render(request, 'pages/tenant/task.html', context)
