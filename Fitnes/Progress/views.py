from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CreateGoalForm, UpdateGoalForm
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