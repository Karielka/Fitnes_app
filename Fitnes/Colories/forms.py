# colories/forms.py
from django import forms
from .models import MealRecord, TimeTable, TrainingSession

class MealRecordFormForCreate(forms.ModelForm):
    class Meta:
        model = MealRecord
        fields = ['product', 'measure',]

class MealRecordFormForEdit(forms.ModelForm):
    class Meta:
        model = MealRecord
        fields = ['product', 'measure', 'category']

class WaterRecordForm(forms.ModelForm):
    class Meta:
        model = MealRecord
        fields = ['measure']

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['breakfast_time', 'lunch_time', 'dinner_time', 'go_to_sleep_time']

class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['day_of_week', 'start_time', 'end_time']