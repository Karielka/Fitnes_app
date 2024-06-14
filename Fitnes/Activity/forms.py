# colories/forms.py
from django import forms
from .models import Sleep

class MealRecordFormForCreate(forms.ModelForm):
    class Meta:
        model = Sleep
        fields = ['date', 'duration', 'notes']
