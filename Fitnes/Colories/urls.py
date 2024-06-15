from django.urls import path

import Colories.views as colories

urlpatterns = [
    path('', colories.index, name='index-colories'),
    path('meal_record/',colories.meal_records_read, name='meal_record_read'),
    path('meal_record/create/', colories.meal_record_create, name='meal_record_create'),
    path('meal_record/update/<int:meal_record_id>/', colories.meal_record_update, name='meal_record_update'),
    path('meal_record/delete/<int:meal_record_id>/', colories.meal_record_delete, name='meal_record_delete'),
    path('colories_dynamic/', colories.colory_dynamic, name='colory_dynamic'),
]
