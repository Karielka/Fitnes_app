from django.shortcuts import render, redirect, get_object_or_404
from .models import MealRecord
from .forms import MealRecordFormForCreate, MealRecordFormForEdit
import plotly.graph_objects as go # type: ignore
from django.http import HttpResponse
from .models import MealRecord, Product, History
from django.contrib.auth.decorators import login_required
import io
from django.contrib.auth.models import User
import datetime
import base64
from Progress.forms import UpdateCurrentWeightForm
from Progress.models import Goal

def index(request):
    meal_record = MealRecord.objects.filter(user=request.user)
    if request.user.is_authenticated:
        user_id = request.user.id
        calories_chart_data = calories_chart(request, user_id)
        macronutrient_chart_data = macronutrient_chart(request, user_id)
        context = {
            'title': 'Страница для учёта Ваших калорий',
            'message': 'Вы находитесь на главной странице Colories',
            'page': 'colories_main',
            'calories_chart_data': calories_chart_data,
            'macronutrient_chart_data': macronutrient_chart_data,
            'mealrecord': meal_record,
        }
    else:
        context = {
            'title': 'Страница для учёта калорий',
            'message': 'Вы находитесь на главной странице Colories',
            'page': 'colories_main',
        }
    return render(request, 'colories/index.html', context)


def get_user_history(user_id, start_date=None, end_date=None):
    user = get_object_or_404(User, pk=user_id)
    histories = user.history.all()

    if start_date:
        histories = histories.filter(date__gte=start_date)
    if end_date:
        histories = histories.filter(date__lte=end_date)

    return histories


@login_required
def calories_chart(request, user_id):
    # Получаем данные о калориях пользователя
    user = get_object_or_404(User, pk=user_id)
    user_history = get_user_history(user_id, start_date=None, end_date=None)

    # Создаем данные для графика
    dates = [record.date for record in user_history]
    calories = [record.total_calories for record in user_history]

    # Создаем график plotly
    fig = go.Figure(data=go.Scatter(x=dates, y=calories))
    fig.update_layout(title="Динамика калорийности",
                      xaxis_title="Дата",
                      yaxis_title="Калории")

    buf = io.BytesIO()
    fig.write_image(buf, format='png')
    buf.seek(0)

    # Возвращаем график в виде base64-строки
    chart_data = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Возвращаем данные о графике в контекст
    return chart_data


@login_required
def macronutrient_chart(request, user_id):
    # Получаем данные о питании пользователя
    user = get_object_or_404(User, pk=user_id)
    user_history = get_user_history(user_id, start_date=None, end_date=None)

    # Создаем данные для графика
    total_proteins = 0
    total_fats = 0
    total_carbohydrates = 0
    for record in user_history:
        total_proteins += record.total_proteins
        total_fats += record.total_fats
        total_carbohydrates += record.total_carbohydrates

    # Создаем график plotly
    labels = ['Белки', 'Жиры', 'Углеводы']
    fig = go.Figure(data=[go.Pie(labels=labels, values=[total_proteins, total_fats, total_carbohydrates])])
    fig.update_layout(title="Процентное соотношение БЖУ")

    buf = io.BytesIO()
    fig.write_image(buf, format='png')
    buf.seek(0)

    # Возвращаем график в виде base64-строки
    chart_data = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Возвращаем данные о графике в контекст
    return chart_data

@login_required
def food_dynamics_view(request):
    # Получаем id текущего пользователя
    user_id = request.user.id
    
    # Получаем графики
    calories_chart_data = calories_chart(request, user_id)
    macronutrient_chart_data = macronutrient_chart(request, user_id)

    # Рендерим шаблон
    return render(request, 'colories/index.html', {
        'calories_chart_data': calories_chart_data,
        'macronutrient_chart_data': macronutrient_chart_data,
    })


def update_history_for_user(user):
    # Получаем или создаем History для пользователя
    today = datetime.date.today() 
    try:
        user_history = user.history.get(date=today)
    except History.DoesNotExist:
        user_history = History.objects.create(
            user=user,
            date=today
        )
    # Обновляем данные в History
    user_history.update_history()









def meal_record_create(request):
    if request.method == 'POST':
        form = MealRecordFormForCreate(request.POST)
        if form.is_valid():
            meal_record = form.save(commit=False)
            meal_record.user = request.user  # Привязка к текущему пользователю
            meal_record.save()
            # Обновляем историю калорий после добавления новой записи
            update_history_for_user(request.user)
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
            update_history_for_user(request.user) # Обновляем историю после редактирования
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
        update_history_for_user(request.user) # Обновляем историю после удаления
        return redirect('meal_record_read')
    context = {
        'title': 'Удалить запись о приёме пищи',
        'meal_record': meal_record,
    }
    return render(request, 'colories/meal_record_delete.html', context)


@login_required
def update_current_weight(request):
    user = request.user
    # Находим последнюю активную цель пользователя
    active_goal = Goal.objects.filter(user=user, status__in=['New', 'In_work']).order_by('-start_date').first()

    if not active_goal:
        return redirect('create_goal')  # Если нет активной цели, перенаправляем на создание цели

    if request.method == 'POST':
        form = UpdateCurrentWeightForm(request.POST, instance=active_goal)
        if form.is_valid():
            form.save()
            return redirect('tracking_current_weight')  # Перенаправляем на профиль пользователя после сохранения
    else:
        form = UpdateCurrentWeightForm(instance=active_goal)
    
    context = {
        'form': form,
        'active_goal': active_goal,
        'for_goal_left': abs(active_goal.current_weight - active_goal.target_weight)
    }
    return render(request, 'colories/weight_tracking.html', context)