# colories/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import MealRecord
from .forms import MealRecordFormForCreate, MealRecordFormForEdit

def index(request):
    #meal_record = MealRecord.objects.filter(user=request.user)
    context = {
        'title': 'Страница для учёта Ваших калорий',
        'message': 'Вы находитесь на главной странице Colories',
        'page': 'colories_main',
        #mealrecord': meal_record
    }
    return render(request, 'colories/index.html', context)

def meal_record_create(request):
    if request.method == 'POST':
        form = MealRecordFormForCreate(request.POST)
        if form.is_valid():
            meal_record = form.save(commit=False)
            meal_record.user = request.user  # Привязка к текущему пользователю
            meal_record.save()
            return redirect('meal_record_read')  # Перенаправление после создания
    else:
        form = MealRecordFormForCreate()
    context = {
        'title': 'Создать запись о приёме пищи',
        'form': form,
    }
    return render(request, 'colories/meal_record_create.html', context)

def meal_records_read(request):
    meal_records = MealRecord.objects.filter(user=request.user)
    context = {
        'title': 'Список записей о приёмах пищи',
        'meal_records': meal_records,
    }
    return render(request, 'colories/meal_record_read.html', context)

def meal_record_update(request, meal_record_id):
    meal_record = get_object_or_404(MealRecord, pk=meal_record_id)
    if request.method == 'POST':
        form = MealRecordFormForEdit(request.POST, instance=meal_record)
        if form.is_valid():
            form.save()
            return redirect('meal_record_read')
    else:
        form = MealRecordFormForEdit(instance=meal_record)
    context = {
        'title': 'Редактировать запись о приёме пищи',
        'form': form,
    }
    return render(request, 'colories/meal_record_update.html', context)

def meal_record_delete(request, meal_record_id):
    meal_record = get_object_or_404(MealRecord, pk=meal_record_id)
    if request.method == 'POST':
        meal_record.delete()
        return redirect('meal_record_read')
    context = {
        'title': 'Удалить запись о приёме пищи',
        'meal_record': meal_record,
    }
    return render(request, 'colories/meal_record_delete.html', context)
