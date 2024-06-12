from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserCaloryProfile
from .forms import UserCaloryProfileForm

@login_required
def profile_edit(request):
    profile = get_object_or_404(UserCaloryProfile, user=request.user)
    if request.method == 'POST':
        form = UserCaloryProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/fitnes/profile/')
    else:
        form = UserCaloryProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})

@login_required
def profile_create(request):
    if request.method == 'POST':
        form = UserCaloryProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('/fitnes/profile/')
    else:
        form = UserCaloryProfileForm()
    return render(request, 'profiles/fill_profile.html', {'form': form})