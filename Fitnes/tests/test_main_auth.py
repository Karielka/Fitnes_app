import pytest
from Main.views import A

def test_class_A():
    assert A.x == 1

def test_main():
    assert 1 == 1

# Параметризация - проверка нескольких тестовых случаев для 1 сценария.
# То есть функция одна, а вариантов значений - много.

# Фикстуры - создают среду для тестрования.
# Например для авторизации пользователя. Очистка + наполнение кэша. 
# Часто используемые данные для тестов. Для упрощения объявления переменных

#conftest.py - файл для структур, необходимых для всего проекта

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

@pytest.fixture
def user(db):
    return User.objects.get_or_create(username='karielka', password='1234')

@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
def test_login(client, user):
    login_url = reverse('login')
    profile_url = reverse('profile')
    response = client.post(login_url, {'username': 'karielka', 'password': '1234'})
    assert response.status_code == 200
    
    #assert response.url == profile_url 

@pytest.mark.django_db
def test_profile_access(client, user):
    profile_url = reverse('profile')
    client.login(username='karielka', password='1234')
    response = client.get(profile_url)# Обращение к 
    assert response.status_code == 302
#можно сделать тоже самое, но с регистрацией + логин и статус 200

#Нет страницы с ошибкой, поэтому только статус 403
# @pytest.mark.django_db
# def test_login_failure(client, user):
#     login_url = reverse('login')
#     response = client.post(login_url, {'username': 'karielka', 'password': '123'})
#     assert response.status_code == 200  
#     assert 'Лох!' == response.content 
