from django.urls import path
from . import views

urlpatterns = [
    path('profile/edit/', views.profile_edit, name='calory_profile_edit'),
    path('profile/create/', views.profile_create, name='profile_create'),
]
