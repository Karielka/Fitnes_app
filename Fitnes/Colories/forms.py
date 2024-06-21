# colories/forms.py
from django import forms
from .models import MealRecord

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