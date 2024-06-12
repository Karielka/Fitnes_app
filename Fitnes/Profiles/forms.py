from django import forms
from .models import UserCaloryProfile

class UserCaloryProfileForm(forms.ModelForm):
    class Meta:
        model = UserCaloryProfile
        fields = ['age', 'gender', 'height', 'weight', 'goal', 'target_weight', 'activity_level', 'target_date']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}, choices=[('male', 'Male'), ('female', 'Female')]),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'goal': forms.Select(attrs={'class': 'form-control'}),
            'target_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'activity_level': forms.Select(attrs={'class': 'form-control'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
