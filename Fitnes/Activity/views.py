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
        'message': 'Вы находитесь на главной странице Activity',
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
def sleep_record_update(request, sleep_record_id):
    sleep_record = get_object_or_404(Sleep, pk=sleep_record_id)
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
def sleep_record_delete(request, sleep_record_id):
    sleep_record = get_object_or_404(Sleep, pk=sleep_record_id)
    if request.method == 'POST':
        sleep_record.delete()
        #update_history_for_user(request.user) # Обновляем историю после удаления
        return redirect('sleep_records_read')
    context = {
        'title': 'Удалить запись о сне',
        'sleep_record': sleep_record,
    }
    return render(request, 'activity/sleep_record_delete.html', context)