from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserCaloryProfile, Profile
from .forms import UserCaloryProfileForm, UserProfileForm
from Progress.models import Goal
from Colories.forms import TimeTableForm 
from Colories.models import TimeTable
from django.forms import modelformset_factory

from Activity.models import TrainingSession
from Activity.forms import TrainingSessionForm

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
    user = request.user
    try:
        profile = user.calory_profile
    except UserCaloryProfile.DoesNotExist:
        profile = UserCaloryProfile.objects.create(user=user)
        
    try:
        time_table = TimeTable.objects.get(user=user)
    except TimeTable.DoesNotExist:
        time_table = TimeTable.objects.create(user=user)

    TrainingSessionFormSet = modelformset_factory(TrainingSession, form=TrainingSessionForm, extra=0, can_delete=True)

    if request.method == 'POST':
        form = UserCaloryProfileForm(request.POST, instance=profile)
        time_table_form = TimeTableForm(request.POST, instance=time_table)
        formset = TrainingSessionFormSet(request.POST, queryset=TrainingSession.objects.filter(time_table=time_table))

        if form.is_valid() and time_table_form.is_valid() and formset.is_valid():
            form.save()
            time_table_form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                if instance.id is None:  # Проверка на пустой id
                    instance.time_table = time_table
                instance.save()
            for instance in formset.deleted_objects:
                instance.delete()
            return redirect('profile')
        else:
            # Вывод ошибок форм в консоль для диагностики
            print(form.errors)
            print(time_table_form.errors)
            print(formset.errors)
            for form in formset:
                print(form.errors)
    else:
        form = UserCaloryProfileForm(instance=profile)
        time_table_form = TimeTableForm(instance=time_table)
        formset = TrainingSessionFormSet(queryset=TrainingSession.objects.filter(time_table=time_table))

    context = {
        'form': form,
        'time_table_form': time_table_form,
        'formset': formset,
    }
    return render(request, 'profiles/calory_profile_edit.html', context)

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