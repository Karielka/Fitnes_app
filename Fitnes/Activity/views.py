from django.shortcuts import render, redirect, get_object_or_404
from .forms import SleepRecordFormForCreate
import plotly.graph_objects as go # type: ignore
from django.http import HttpResponse
from .models import Sleep, Exercise
from django.contrib.auth.decorators import login_required
import io
from django.contrib.auth.models import User
import datetime
import base64

def index(request):
    context = {
        'title': 'Страница Ваших физических активностей',
        'message': 'Тренировки',
        'page': 'activity_main',
    }
    return render(request, 'activity/index.html', context)

@login_required
def sleep_record_create(request):
    if request.method == 'POST':
        form = SleepRecordFormForCreate(request.POST)
        if form.is_valid():
            sleep_record = form.save(commit=False)
            sleep_record.user = request.user
            sleep_record.calories_burned = 40 #заглушка (нужна формула)
            sleep_record.save()
            #update_history_for_user(request.user)
            return redirect('sleep_records_read')
    else:
        form = SleepRecordFormForCreate()
    context = {
        'title': "Создайте запись о своём сне",
        'form': form,
    }
    return render(request, 'activity/sleep_record_create.html', context)

@login_required
def sleep_records_read(request):
    sleep_records = Sleep.objects.filter(user=request.user)
    context = {
        'title': 'Список записей о сне',
        'sleep_records': sleep_records,
    }
    return render(request, 'activity/sleep_records_read.html', context)

@login_required
def sleep_record_update(request, sleep_id):
    sleep_record = get_object_or_404(Sleep, pk=sleep_id)
    if request.method == 'POST':
        form = SleepRecordFormForCreate(request.POST, instance=sleep_record)
        if form.is_valid():
            form.save()
            #update_history_for_user(request.user) # Обновляем историю после редактирования
            return redirect('sleep_records_read')
    else:
        form = SleepRecordFormForCreate(instance=sleep_record)
    context = {
        'title': 'Редактировать запись о сне',
        'form': form,
    }
    return render(request, 'activity/sleep_record_update.html', context)

@login_required
def sleep_record_delete(request, sleep_id):
    sleep_record = get_object_or_404(Sleep, pk=sleep_id)
    if request.method == 'POST':
        sleep_record.delete()
        #update_history_for_user(request.user) # Обновляем историю после удаления
        return redirect('sleep_records_read')
    context = {
        'title': 'Удалить запись о сне',
        'sleep_record': sleep_record,
    }
    return render(request, 'activity/sleep_record_delete.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Exercise
from .forms import ExerciseForm
from Profiles.models import Profile

@login_required
def exercise_list(request):
    try:
        expert = request.user.expert_profile
    except Profile.DoesNotExist:
        expert = None
    exercises = Exercise.objects.filter(user=request.user)
    context = {
        'title': 'Список упражнений',
        'exercises': exercises,
        'expert': expert,
    }
    return render(request, 'activity/exercise_list.html', context)

@login_required
def exercise_create(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            return redirect('exercise_list')
    else:
        form = ExerciseForm()
    context = {
        'title': 'Создать упражнение',
        'form': form,
        'exercise': None, 
    }
    return render(request, 'activity/exercise_form.html', context)

@login_required
def exercise_update(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect('exercise_list')
    else:
        form = ExerciseForm(instance=exercise)
    context = {
        'title': 'Редактировать упражнение',
        'form': form,
        'exercise': exercise,  # Передаем объект упражнения в контекст
    }
    return render(request, 'activity/exercise_form.html', context)


@login_required
def exercise_delete(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        exercise.delete()
        return redirect('exercise_list')
    context = {
        'title': 'Удалить упражнение',
        'exercise': exercise,
    }
    return render(request, 'activity/exercise_confirm_delete.html', context)

@login_required
def exercise_detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    context = {
        'title': 'Детали упражнения',
        'exercise': exercise,
    }
    return render(request, 'activity/exercise_detail.html', context)
