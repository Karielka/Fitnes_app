from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

#from tasks.models import Profile, Task

def index(request):
    context = {
        'title': 'Страница для учёта Ваших колорий',
        'message': 'Вы находитесь на главной странице Colories',
        'page': 'colories_main',
    }
    return render(request, 'colories/index.html', context)