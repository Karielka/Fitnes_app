from django.urls import path
from . import views

urlpatterns = [
    path('caloryprofile/edit/', views.calory_profile_edit, name='calory_profile_edit'),
    path('profile/create/', views.profile_create, name='profile_create'),

    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/', views.profile, name='profile'),
]
