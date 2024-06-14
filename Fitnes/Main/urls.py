from django.urls import path

import Main.views as main

urlpatterns = [
    path('', main.index, name='index'),
    path('register/', main.register, name='register'),
    path('login/', main.login_view, name='login'),
    path('logout/', main.logout_view, name='logout'),
    path('password_reset/', main.password_reset, name='password_reset'),
]