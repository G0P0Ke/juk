from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import DiscussionCreationForm
from .models import Discussion, Forum
from datetime import datetime


def profile_view(request):
    context = {"user": request.user, }
    return render(request, 'profile.html', context)


def forum(request, id):
    context = {"user": request.user, }
    return render(request, 'forum.html', context)


def discussion(request):
    context = {"user": request.user, }
    return render(request, 'discussion.html', context)


@login_required
def cr_discussion(request, id):
    context = {
        "user": request.user,
        "done": False,
        "error": False,
        "form": DiscussionCreationForm(),
    }
    if request.method == 'POST':
        form = DiscussionCreationForm(request.POST)
        if form.is_valid():
            model = Discussion()
            parent_forum = Forum.objects.get(id=id)
            if not form.anonymous:
                model.author = request.user
            model.category = form.category
            model.cr_date = datetime.now()
            model.description = form.description
            model.theme = form.theme
            model.forum = parent_forum
            context.update({
                "done": True,
            })
        else:
            context.update({
                "form": DiscussionCreationForm(request.POST),
                "error": True,
            })

    return render(request, 'cr_discussion.html', context)
