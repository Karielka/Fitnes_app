from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

#from tasks.models import Profile, Task

def index(request):
    context = {
        'title': 'Страница наших экспертов',
        'message': 'Эксперты',
        'page': 'expertise_main',
    }
    return render(request, 'expertise/index.html', context)

from django.contrib.auth.decorators import login_required
from .models import ExpertTimetable
from .forms import ExpertTimetableForm
from Profiles.models import ExpertProfile, Profile

@login_required
def expert_timetable_list(request):
    # Получаем профиль эксперта, связанный с текущим пользователем
    expert_profile = ExpertProfile.objects.get(user=request.user)
    timetables = ExpertTimetable.objects.filter(expert=expert_profile)
    try:
        expert = request.user.expert_profile
    except Profile.DoesNotExist:
        expert = None
    context = {
        'title': 'Расписание тренера',
        'timetables': timetables,
        'expert': expert
    }
    return render(request, 'expertise/expert_timetable_list.html', context)


@login_required
def expert_timetable_create(request):
    if request.method == 'POST':
        form = ExpertTimetableForm(request.POST)
        if form.is_valid():
            timetable = form.save(commit=False)
            timetable.expert = request.user
            timetable.save()
            return redirect('timetable_list')
    else:
        form = ExpertTimetableForm()
    context = {
        'title': 'Создать расписание',
        'form': form,
    }
    return render(request, 'expertise/expert_timetable_form.html', context)

@login_required
def expert_timetable_update(request, pk):
    timetable = get_object_or_404(ExpertTimetable, pk=pk)
    if request.method == 'POST':
        form = ExpertTimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            form.save()
            return redirect('timetable_list')
    else:
        form = ExpertTimetableForm(instance=timetable)
    context = {
        'title': 'Редактировать расписание',
        'form': form,
    }
    return render(request, 'expertise/expert_timetable_form.html', context)

@login_required
def expert_timetable_delete(request, pk):
    timetable = get_object_or_404(ExpertTimetable, pk=pk)
    if request.method == 'POST':
        timetable.delete()
        return redirect('timetable_list')
    context = {
        'title': 'Удалить расписание',
        'timetable': timetable,
    }
    return render(request, 'expertise/expert_timetable_confirm_delete.html', context)

@login_required
def expert_timetable_detail(request, pk):
    timetable = get_object_or_404(ExpertTimetable, pk=pk)
    context = {
        'title': 'Детали расписания',
        'timetable': timetable,
    }
    return render(request, 'expertise/expert_timetable_detail.html', context)