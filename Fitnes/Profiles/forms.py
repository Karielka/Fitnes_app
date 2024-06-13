from django import forms
from .models import UserCaloryProfile

class UserCaloryProfileForm(forms.ModelForm):
    class Meta:
        model = UserCaloryProfile
        fields = ['birthdate', 'gender', 'height', 'activity_level']
        widgets = {
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}, choices=[('male', 'Male'), ('female', 'Female')]),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'activity_level': forms.Select(attrs={'class': 'form-control'}),
        }
