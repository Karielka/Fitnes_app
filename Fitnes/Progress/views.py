from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CreateGoalForm, UpdateGoalForm, UpdateCurrentWeightForm
from .models import Goal, WeightHistory
import plotly.graph_objects as go # type: ignore
import io
import base64
from django.contrib.auth.models import User

@login_required
def index(request):
    goals = Goal.objects.filter(user=request.user)
    context = {
        'title': 'Страница Вашего прогресса',
        'message': 'Вы находитесь на главной странице Progress',
        'page': 'progress_main',
        'goals': goals,
    }
    return render(request, 'progress/index.html', context)

@login_required
def create_goal(request):
    if request.method == 'POST':
        form = CreateGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.current_weight = goal.start_weight
            goal.save()
            return redirect('index-progress') 
    else:
        form = CreateGoalForm()
    return render(request, 'progress/create_goal.html', {'form': form})

@login_required
def edit_goal(request, pk):
    goal = get_object_or_404(Goal, pk=pk)
    if request.method == 'POST':
        form = UpdateGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('index-progress')
    else:
        form = UpdateGoalForm(instance=goal)
    return render(request, 'progress/edit_goal.html', {'form': form})

@login_required
def delete_goal(request, pk):
    goal = get_object_or_404(Goal, pk=pk)
    if request.method == 'POST':
        goal.delete()
        return redirect('index-progress')
    return render(request, 'progress/delete_goal.html', {'goal': goal})

@login_required
def update_current_weight(request):
    user = request.user
    # Находим последнюю активную цель пользователя
    active_goal = Goal.objects.filter(user=user, status__in=['New', 'In_work']).order_by('-start_date').first()
    user_id = request.user.id
    if not active_goal:
        return redirect('create_goal')  # Если нет активной цели, перенаправляем на создание цели

    if request.method == 'POST':
        form = UpdateCurrentWeightForm(request.POST, instance=active_goal)
        if form.is_valid():
            form.save()
            return redirect('tracking_current_weight')  # Перенаправляем на профиль пользователя после сохранения
    else:
        form = UpdateCurrentWeightForm(instance=active_goal)
    weight_chart_data = weight_chart(request, user_id)
    context = {
        'form': form,
        'active_goal': active_goal,
        'for_goal_left': abs(active_goal.current_weight - active_goal.target_weight),
        'weight_chart_data': weight_chart_data  # Передаем данные графика в контекст
    }
    return render(request, 'progress/weight_tracking.html', context)

def weight_chart(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    history = user.weight_history.all().order_by('date') # Получаем историю изменений
    # Создаем данные для графика
    dates = [record.date for record in history]
    weights = [record.weight for record in history]

    active_goal = Goal.objects.filter(user=user, status__in=['New', 'In_work']).order_by('-start_date').first()
    target_weight = active_goal.target_weight if active_goal else None

    # Создаем график plotly
    fig = go.Figure(data=go.Scatter(
    x=dates, 
    y=weights, 
    mode='lines+markers', 
    marker=dict(size=8, color='darkslategray'), 
    line=dict(color='rgb(36, 56, 23)', width=2), #  Добавляем стили линии
    fillcolor='#f0f0f0',  # Прозрачный фон области графика
    ))
    fig.update_layout(
                      plot_bgcolor='#f6f6f6',  # фон области графика
                      paper_bgcolor="#f6f6f6",  # Цвет фона 
                      showlegend=False
                      )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='Grey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Grey')
    # Добавляем линию цели, если она есть
    if target_weight is not None:
        fig.add_trace(go.Scatter(
            x=dates,  # Используем те же даты, что и для графика веса
            y=[target_weight] * len(dates),  # Создаем список значений цели для каждой даты
            mode='lines',  # Только линия
            line=dict(color='red', dash='dash'),  # Красная пунктирная линия
            name='Цель'  # Добавляем название для легенды (если она включена)
        ))
    buf = io.BytesIO()
    fig.write_image(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.getvalue()).decode('utf-8') # Возвращаем график в виде base64-строки
    return chart_data
