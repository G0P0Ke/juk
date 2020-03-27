from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from tenant.forms import EditProfileForm

# Create your views here.


@login_required
def profile(request):
    context = {
        'user': request.user,
    }
    if request.method == 'POST':
        editprof = EditProfileForm(request.POST, instance=request.user)
        if editprof.is_valid():
            editprof.save()
            context.update({
                'editprof': editprof,
            })
        return redirect('profile')
    else:
        editprof = EditProfileForm(instance=request.user)

    context.update({
        'editprof': editprof,
    })

    return render(request, 'user_profile/profile.html', context)