# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15)
    USER_TYPE_CHOICES = [
        ('user', 'User'),
        ('expert', 'Expert'),
    ]
    type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username','email', 'phone', 'password1', 'password2', 'type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

            # Создаем профиль для пользователя
            profile = Profile.objects.create(
                user=user,
                type=self.cleaned_data['type']
            )
            profile.save()

        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': 'Имя пользователя'
        }),
        label=''
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль'
        }),
        label=''
    )
