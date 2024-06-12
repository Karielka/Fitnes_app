# colories/forms.py
from django import forms
from .models import MealRecord
from Profiles.models import UserCaloryProfile

class MealRecordFormForCreate(forms.ModelForm):
    class Meta:
        model = MealRecord
        fields = ['product', 'measure', 'category']

class MealRecordFormForEdit(forms.ModelForm):
    class Meta:
        model = MealRecord
        fields = ['product', 'measure', 'category']

class UpdateCurrentWeightForm(forms.ModelForm):
    class Meta:
        model = UserCaloryProfile
        fields = ['weight']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Текущий вес'}),
        }
        labels = {
            'weight': 'Текущий вес (кг)',
        }