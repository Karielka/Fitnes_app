from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, LoginForm, PasswordResetForm
from django.contrib.auth.hashers import make_password

class A:
    x = 1
    
def index(request):
    context = {
        'title': 'Главная страница приложения',
        'message': 'Вы находитесь на главной странице сайта',
        'page': 'main',
    }
    return render(request, 'main/index.html', context)

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            new_password = form.cleaned_data.get('new_password1')
            user = User.objects.get(username=username)
            user.password = make_password(new_password)
            user.save()
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = PasswordResetForm()
    return render(request, 'main/password_reset.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
        'page': 'register'
    }
    return render(request, 'main/register.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('profile')
    else:
        form = LoginForm()
    context = {
        'form': form,
        'page': 'login',
    }
    return render(request, 'main/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')