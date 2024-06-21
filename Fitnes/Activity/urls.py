from django.urls import path
import Activity.views as activity

urlpatterns = [
    path('', activity.index, name='index-activity'),
    path('sleep_records_read/',activity.sleep_records_read, name='sleep_records_read'),
    path('sleep_record/create/', activity.sleep_record_create, name='sleep_record_create'),
    path('sleep_record/update/<int:sleep_id>/', activity.sleep_record_update, name='sleep_record_update'),
    path('sleep_record/delete/<int:sleep_id>/', activity.sleep_record_delete, name='sleep_record_delete'),
]