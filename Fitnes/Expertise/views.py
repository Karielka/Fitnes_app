from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

#from tasks.models import Profile, Task

def index(request):
    context = {
        'title': 'Страница наших экспертов',
        'message': 'Тренировки',
        'page': 'expertise_main',
    }
    return render(request, 'expertise/index.html', context)