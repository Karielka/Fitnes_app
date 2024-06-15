from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserCaloryProfile, Profile
from .forms import UserCaloryProfileForm, UserProfileForm
from Progress.models import Goal

@login_required
def profile_edit(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        initial_data = {
            'phone': profile.phone,
        }
        form = UserProfileForm(instance=user, initial=initial_data)
    return render(request, 'profiles/profile_edit.html', {'form': form})

@login_required
def calory_profile_edit(request):
    profile = get_object_or_404(UserCaloryProfile, user=request.user)
    if request.method == 'POST':
        form = UserCaloryProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserCaloryProfileForm(instance=profile)
    return render(request, 'profiles/calory_profile_edit.html', {'form': form})

@login_required
def profile_create(request):
    if request.method == 'POST':
        form = UserCaloryProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = UserCaloryProfileForm()
    return render(request, 'profiles/fill_profile.html', {'form': form})

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    try:
        calory_profile = request.user.calory_profile
    except UserCaloryProfile.DoesNotExist:
        calory_profile = None

    user = request.user
    active_goal = Goal.objects.filter(user=user, status__in=['New', 'In_work']).order_by('-start_date').first()

    context = {
        'profile': profile,
        'calory_profile': calory_profile,
        'page': 'profile',
        'goal': active_goal,
    }
    return render(request, 'profiles/profile.html', context)