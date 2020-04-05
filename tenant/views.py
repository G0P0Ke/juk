from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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
def cr_discussion(request):
    context = {"user": request.user, }
    return render(request, 'cr_discussion.html', context)
