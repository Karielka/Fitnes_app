from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

#from tasks.models import Profile, Task

def index(request):
    context = {
        'title': 'Страница Ваших доставок',
        'message': 'Вы находитесь на главной странице Delivery',
        'page': 'delivery_main',
    }
    return render(request, 'delivery/index.html', context)