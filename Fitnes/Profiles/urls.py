from django.urls import path
from . import views

urlpatterns = [
    path('caloryprofile/edit/', views.calory_profile_edit, name='calory_profile_edit'),
    path('profile/create/', views.profile_create, name='profile_create'),

    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/', views.profile, name='profile'),
    path('expert/create/', views.create_expert_profile, name='create_expert_profile'),
    path('expert/<int:pk>/edit/', views.edit_expert_profile, name='edit_expert_profile'),
    path('expert/<int:pk>/', views.view_expert_profile, name='view_expert_profile'),
]
