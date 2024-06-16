from django.shortcuts import render, redirect, get_object_or_404
from .models import MealRecord
from .forms import MealRecordFormForCreate, MealRecordFormForEdit, WaterRecordForm
import plotly.graph_objects as go # type: ignore
from django.http import HttpResponse
from .models import MealRecord, Product, History
from django.contrib.auth.decorators import login_required
import io
from django.contrib.auth.models import User
import base64
from Activity.models import Sleep, Exercise
from datetime import datetime, timedelta, date
from Profiles.models import UserCaloryProfile

def colory_dynamic(request):
    context = {
        'title': 'Страница для отображения изменения калорий',
        'message': 'Вы находитесь на странице Colories_dynamic',
        'page': 'colories_dynamic',
    }
    return render(request, 'colories/dynamic.html', context)

def calculate_today_sleep(user):
    today = date.today()
    start_of_today = datetime.combine(today, datetime.min.time())
    end_of_today = datetime.combine(today, datetime.max.time())
    total_sleep_duration = timedelta()
    sleep_records = Sleep.objects.filter(user=user, date=today)
    for record in sleep_records:
        # Начало и конец сна
        sleep_start = datetime.combine(record.date, datetime.min.time())
        sleep_end = sleep_start + record.duration
        # Пересечение сна с сегодняшним днем
        if sleep_end > start_of_today and sleep_start < end_of_today:
            # Начало периода внутри сегодняшнего дня
            if sleep_start < start_of_today:
                sleep_start = start_of_today
            # Конец периода внутри сегодняшнего дня
            if sleep_end > end_of_today:
                sleep_end = end_of_today
            total_sleep_duration += (sleep_end - sleep_start)
    # Возвращаем продолжительность сна в секундах, минутах и часах
    total_sleep_seconds = total_sleep_duration.total_seconds()
    sleep_hours = int(total_sleep_seconds // 3600)
    sleep_minutes = int((total_sleep_seconds % 3600) // 60)
    return sleep_hours, sleep_minutes

def per_day_colories(user_name):
    profile = UserCaloryProfile.objects.get(user=user_name)
    age = date.today().year - profile.birthdate.year
    if (profile.gender.lower() == 'male'):
        need = 10 * profile.current_weight + (6.25 * profile.height) - (5 * age) + 5
    else:
        need = 10 * profile.current_weight + (6.25 * profile.height) - (5 * age) - 161
    return need

def index(request):
    meal_record = MealRecord.objects.filter(user=request.user)
    if request.user.is_authenticated:
        user_id = request.user.id
        calories_chart_data = calories_chart(request, user_id)
        todays_meals = MealRecord.objects.filter(user=request.user, meal_time__date=date.today())
        breakfast_data = get_meal_data(todays_meals, 'Breakfast')
        lunch_data = get_meal_data(todays_meals, 'Dinner')
        dinner_data = get_meal_data(todays_meals, 'Supper')
        snack_data = get_meal_data(todays_meals, 'Snack')
        water_data = get_meal_data(todays_meals, 'Water')

        proteins_sum = breakfast_data['proteins'] + lunch_data['proteins'] + dinner_data['proteins'] + snack_data['proteins']
        fats_sum = breakfast_data['fats'] + lunch_data['fats'] + dinner_data['fats'] + snack_data['fats']
        carbs_sum = breakfast_data['carbs'] + lunch_data['carbs'] + dinner_data['carbs'] + snack_data['carbs']
        calories_sum = breakfast_data['calories'] + lunch_data['calories'] + dinner_data['calories'] + snack_data['calories']
        
        total_macros = proteins_sum + fats_sum + carbs_sum

        protein_percent = (proteins_sum / total_macros) * 100 if total_macros else 0
        fat_percent = (fats_sum / total_macros) * 100 if total_macros else 0
        carb_percent = (carbs_sum / total_macros) * 100 if total_macros else 0
        macronutrient_chart_data = macronutrient_chart(request, user_id, proteins_sum, fats_sum, carbs_sum)
        # Вычисляем количество сна за сегодняшний день
        sleep_hours, sleep_minutes = calculate_today_sleep(request.user)

        needed = per_day_colories(request.user)

        context = {
            'title': 'Страница для учёта Ваших калорий',
            'message': 'Вы находитесь на главной странице Colories',
            'page': 'colories_main',
            'calories_chart_data': calories_chart_data,
            'macronutrient_chart_data': macronutrient_chart_data,
            'mealrecord': meal_record,
            'breakfast_data': breakfast_data,
            'lunch_data': lunch_data,
            'dinner_data': dinner_data,
            'snack_data': snack_data,
            'water_data': water_data,  # Передаем данные о воде
            'proteins_sum': proteins_sum,  # Передача суммарных значений
            'fats_sum': fats_sum,
            'carbs_sum': carbs_sum,
            'calories_sum': calories_sum,
            'protein_percent': protein_percent,
            'fat_percent': fat_percent,
            'carb_percent': carb_percent,
            'sleep_hours': sleep_hours,  # Передаем количество сна в часах
            'sleep_minutes': sleep_minutes,  # Передаем количество сна в минутах
            'needed': needed,
            'ostatok': needed - calories_sum,
        }
    else:
        context = {
            'title': 'Страница для учёта калорий',
            'message': 'Вы находитесь на главной странице Colories',
            'page': 'colories_main',
        }
    return render(request, 'colories/index.html', context)

def get_meal_data(meals, category):
    total_proteins = 0
    total_fats = 0
    total_carbs = 0
    total_calories = 0
    water_l = 0  # Добавленная переменная для воды
    for meal in meals:
        if meal.category == category:
            if meal.product.name.lower() == "вода":  # Проверка на "вода" в нижнем регистре
                water_l += meal.measure  # Суммируем миллилитры воды
            else:
                total_proteins += meal.product.proteins_per_unit * meal.measure
                total_fats += meal.product.fats_per_unit * meal.measure
                total_carbs += meal.product.carbohydrates_per_unit * meal.measure
                total_calories += meal.product.calories_per_unit * meal.measure
    return {
        'proteins': total_proteins,
        'fats': total_fats,
        'carbs': total_carbs,
        'calories': total_calories,
        'water_l': water_l # Добавлен ключ water_l
    }

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
def macronutrient_chart(request, user_id, proteins_sum, fats_sum, carbs_sum):
    # Создаем график plotly
    colors = ['rgb(248, 195, 37)', 'rgb(93, 161, 48)', 'rgb(36, 56, 23)']  
    fig = go.Figure(data=[go.Pie(values=[proteins_sum, fats_sum, carbs_sum],
                                  marker=dict(colors=colors),
                                  showlegend=False,
                                  textinfo='none')]) 
    fig.update_layout(
        paper_bgcolor="#f0f0f0",  # Цвет фона графика
        plot_bgcolor="#f0f0f0"  # Цвет области графика
    )
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
    today = date.today() 
    try:
        user_history = user.history.get(date=today)
    except History.DoesNotExist:
        user_history = History.objects.create(
            user=user,
            date=today
        )
    # Обновляем данные в History
    user_history.update_history()

@login_required
def meal_record_create(request):
    category = request.GET.get('category', '')  # Получаем значение категории из GET параметров
    water_product = Product.objects.get(name='Вода')  # Получаем продукт "Вода"
    if category == 'Water':
        form_class = WaterRecordForm
        title = 'Создать запись о приёме воды'
        product = water_product
    else:
        form_class = MealRecordFormForCreate
        title = 'Создать запись о приёме пищи'
        product = None
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            meal_record = form.save(commit=False)
            meal_record.user = request.user
            meal_record.category = category if category else request.POST.get('category')  # Получаем значение категории
            if product:
                meal_record.product = product  # Задаем продукт "Вода", если это категория "Water"
            meal_record.save()
            update_history_for_user(request.user)
            return redirect('meal_record_read')
    else:
        form = form_class()
    context = {
        'title': title,
        'form': form,
        'category': category  # Передаем категорию в контексте
    }
    return render(request, 'colories/meal_record_create.html', context)

@login_required
def meal_records_read(request):
    meal_records = MealRecord.objects.filter(user=request.user)
    context = {
        'title': 'Список записей о приёмах пищи',
        'meal_records': meal_records,
    }
    return render(request, 'colories/meal_record_read.html', context)

@login_required
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

@login_required
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