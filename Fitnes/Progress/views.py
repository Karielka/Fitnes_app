from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

#from tasks.models import Profile, Task

def index(request):
    context = {
        'title': 'Страница Вашего прогресса',
        'message': 'Вы находитесь на главной странице Progress',
        'page': 'progress_main',
    }
    return render(request, 'progress/index.html', context)