from django import forms
from .models import Goal

class CreateGoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['description', 'start_weight', 'target_weight', 'start_date', 'end_date']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Цель'}),
            'start_weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Текущий вес'}),
            'target_weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Желаемый вес'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class UpdateGoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['description', 'current_weight', 'target_weight', 'end_date',]
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Цель'}),
            'current_weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Текущий вес'}),
            'target_weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Желаемый вес'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class UpdateCurrentWeightForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['current_weight']
        widgets = {
            'current_weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Текущий вес'}),
        }
        labels = {
            'current_weight': 'Текущий вес (кг)',
        }