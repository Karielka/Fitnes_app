from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index-progress'),
    path('goal/create/', views.create_goal, name='create_goal'),
    path('goal/edit/<int:pk>/', views.edit_goal, name='edit_goal'),
    path('goal/delete/<int:pk>/', views.delete_goal, name='delete_goal'),
    path('tracking-weight/', views.update_current_weight, name='tracking_current_weight'),
    path('users_rating_read/', views.users_rating_read, name='users_rating_read'),
    path('fail_goal/<int:pk>/', views.fail_goal, name='fail_goal'),
]
