from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

#from tasks.models import Profile, Task

def index(request):
    context = {
        'title': 'Главная страница приложения',
        'message': 'Вы находитесь на главной странице сайта',
        'page': 'main',
    }
    return render(request, 'main/index.html', context)