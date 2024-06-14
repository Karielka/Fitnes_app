from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CreateGoalForm, UpdateGoalForm, UpdateCurrentWeightForm
from .models import Goal

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
    return render(request, 'progress/weight_tracking.html', context)