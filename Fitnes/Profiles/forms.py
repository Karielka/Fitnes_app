from django import forms
from .models import UserCaloryProfile, ExpertProfile
from django.contrib.auth.models import User

class ExpertProfileForm(forms.ModelForm):
    class Meta:
        model = ExpertProfile
        fields = ['nickname', 'experience_years', 'price_per_hour']

class UserCaloryProfileForm(forms.ModelForm):
    birthdate = forms.CharField(required=True, label='', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    height = forms.CharField(required=True, label='', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    current_weight = forms.CharField(required=True, label='', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        label='',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary (little or no exercise)'),
        ('light', 'Lightly active (light exercise/sports 1-3 days/week)'),
        ('moderate', 'Moderately active (moderate exercise/sports 3-5 days/week)'),
        ('active', 'Very active (hard exercise/sports 6-7 days a week)'),
        ('super_active', 'Super active (very hard exercise/sports & physical job)'),
    ]

    activity_level = forms.ChoiceField(
        choices=ACTIVITY_LEVEL_CHOICES,
        label='',
        widget=forms.Select(attrs={'class': 'form-control'})
    )    
    class Meta:
        model = UserCaloryProfile
        fields = ['birthdate', 'gender', 'height', 'current_weight', 'activity_level']

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Почта'
    }))
    phone = forms.CharField(max_length=15, label='', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Номер телефона'
    }))
    username = forms.CharField(max_length=150, label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.profile.phone = self.cleaned_data['phone']
            user.profile.save()
        return user