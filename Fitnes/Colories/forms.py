# colories/forms.py
from django import forms
from .models import MealRecord, TimeTable

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
    breakfast_time = forms.TimeField(label='', widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    lunch_time = forms.TimeField(label='', widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    dinner_time = forms.TimeField(label='', widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    go_to_sleep_time = forms.TimeField(label='', widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))

    class Meta:
        model = TimeTable
        fields = ['breakfast_time', 'lunch_time', 'dinner_time', 'go_to_sleep_time']