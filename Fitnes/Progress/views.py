from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CreateGoalForm, UpdateGoalForm, UpdateCurrentWeightForm
from .models import Goal, WeightHistory, Achievement, UserAchievement, UserRating
import plotly.graph_objects as go # type: ignore
import io
import base64
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import F, ExpressionWrapper, FloatField, Max, Case, When, IntegerField, Window
from django.db.models.functions import RowNumber, DenseRank
from Profiles.models import UserCaloryProfile
from django.contrib import messages

@login_required
def fail_goal(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    goal.status = 'Failed'
    goal.save()
    return redirect('index-progress')

@login_required
def index(request):
    if request.method == 'POST':
        achievement_id = request.POST.get('achievement_id')
        if achievement_id:
            return claim_achievement(request, achievement_id)
    # Обновляем достижения пользователя
    #Не работает!
    check_user_achievements(request.user)

    goals = Goal.objects.filter(user=request.user) #цели
    main_goal = goals.filter(status__in=['New', 'In_work']).first()
    for goal in goals:
        goal.update_status_by_time()

    current_goal = goals.filter(status__in=['New', 'In_work']).first()
    if main_goal and (not (current_goal)):
        messages.success(request, f"Вы завершили цель: {main_goal.description}")
        print('цель завершена')
    historical_goals = list(reversed((goals.exclude(status__in=['New', 'In_work']))))
    all_achievements = Achievement.objects.all() 
    user_achievements = UserAchievement.objects.filter(user=request.user)
    user_achievements_dict = {x.achievement.id: x for x in user_achievements}
    achievements_data = []
    have = 0
    for achievement in all_achievements:
        data = {
            'id': achievement.id,
            'title': achievement.title,
            'description': achievement.description,
            'icon': achievement.icon,
            'points': achievement.points,
            'status': 'Ещё нужно потрудиться',
            'claimed': False,
            'completed': False,
            'need': achievement.needed_for_reach,
        }
        try:
            have = eval(achievement.rule)
            if have is None:
                have = 0
            else: 
                have = float(have)
            data['have'] = have
            progress = int((have / achievement.needed_for_reach) * 100) if achievement.needed_for_reach != 0 else 0  # Вычисление процента выполнения
            data['progress'] = progress
        except Exception as e:
            print(f"Error evaluating rule for achievement {achievement.id}: {e}")

        if achievement.id in user_achievements_dict:
            user_achievement = user_achievements_dict[achievement.id]
            #Дополнительная проверка (функция не работаёт)
            if have >= achievement.needed_for_reach:
                user_achievement.completed = True
                user_achievement.save()
            if ((user_achievement.completed) or (user_achievement.claimed)):
                data['status'] = f"Достигнуто {user_achievement.date_earned}"
                data['completed'] = user_achievement.completed
            if user_achievement.claimed:
                data['claimed'] = user_achievement.claimed
        achievements_data.append(data)

    context = {
        'title': 'Страница Вашего прогресса',
        'message': 'Вы находитесь на главной странице Progress',
        'page': 'progress_main',
        'current_goal': current_goal,
        'historical_goals': historical_goals,
        'achievements_data': achievements_data,
    }
    return render(request, 'progress/index.html', context)

@login_required
def claim_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, id=achievement_id)
    user_achievement, created = UserAchievement.objects.get_or_create(
        user=request.user, 
        achievement=achievement,
        defaults={'claimed': False}
    )
    if not created and not user_achievement.claimed:
        user_achievement.claimed = True
        user_achievement.save()
    # Ensure the user has a UserRating profile, create it if not exists
    user_rating, created = UserRating.objects.get_or_create(user=request.user)
    if created:
        # Initialize the new UserRating profile with default values
        user_rating.rating = 0
        user_rating.save()
    # Update the user's rating
    user_rating.update_rating()
    return redirect('index-progress')

def check_user_achievements(user):
    achievements = Achievement.objects.all()
    for achievement in achievements:
        user_achievement, created = UserAchievement.objects.get_or_create(
            user=user, 
            achievement=achievement,
            defaults={'claimed': False, 'completed': False}
        )
        try:
            have = eval(achievement.rule)
            if have is None:
                have = 0
            else: have = float(have)
            print()
            print(have, achievement.needed_for_reach)
            if have >= achievement.needed_for_reach:
                user_achievement.completed = True
                user_achievement.save()
            print(user.achievement.completed)
        except Exception as e:
            print('No')
            #print(f"Error evaluating rule for achievement {achievement.id}: {e}")

@login_required
def users_rating_read(request):
    user_ratings = UserRating.objects.all().order_by('-rating')
    context = {
        'user_ratings': user_ratings,
    }
    return render(request, 'progress/users_rating_read.html', context)

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

@login_required
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
    chart = fig.to_html
    return chart