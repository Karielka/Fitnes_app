from django.urls import path

import Expertise.views as expertise

urlpatterns = [
    path('', expertise.index, name='index-expertise'),
    
    path('timetables/', expertise.expert_timetable_list, name='timetable_list'),
    path('timetables/create/', expertise.expert_timetable_create, name='timetable_create'),
    path('timetables/<int:pk>/update/', expertise.expert_timetable_update, name='timetable_update'),
    path('timetables/<int:pk>/delete/', expertise.expert_timetable_delete, name='timetable_delete'),
    path('timetables/<int:pk>/', expertise.expert_timetable_detail, name='timetable_detail'),
]