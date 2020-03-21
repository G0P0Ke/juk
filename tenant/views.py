from django.shortcuts import render


def profile_view(request):
    context = {"user": request.user, }
    return render(request, 'profile.html', context)
