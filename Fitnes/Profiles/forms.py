from django import forms
from .models import UserCaloryProfile
from django.contrib.auth.models import User

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

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Почта'
    }))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Номер телефона'
    }))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
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