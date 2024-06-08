from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

#from tasks.models import Profile, Task

def index(request):
    context = {
        'title': 'Страница Ваших физических активностей',
        'message': 'Вы находитесь на главной странице Activity',
        'page': 'activity_main',
    }
    return render(request, 'activity/index.html', context)