# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from Profiles.models import Profile

class PasswordResetForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Повторите новый пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('Пароли не совпадают.')

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем не существует.')
        return username
    
class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=15, 
    label='',
    widget=forms.TextInput(attrs={
            "class":"myfield1",
            'autofocus': True,
            'placeholder': 'Имя пользователя'
        }),
    )

    email = forms.CharField(max_length=15,
    label='',
    widget=forms.TextInput(attrs={
            "class":"myfield1",
            'autofocus': True,
            'placeholder': 'Почта'
        }),                        
    )

    phone = forms.CharField(max_length=15, 
    label='',
    widget=forms.TextInput(attrs={
            "class":"myfield1",
            'autofocus': True,
            'placeholder': 'Номер телефона'
        }), 
    )

    password1 = forms.CharField(strip=False, 
    label='',
    widget=forms.PasswordInput(attrs={
            "class":"myfield2",
            'autofocus': True,
            'placeholder': 'Пароль'
        }), 
    )

    password2 = forms.CharField(strip=False, 
    label='',
    widget=forms.PasswordInput(attrs={
            "class":"myfield2",
            'autofocus': True,
            'placeholder': 'Повторить пароль',
        }), 
    )    

    USER_TYPE_CHOICES = [
        ('user', 'User'),
        ('expert', 'Expert'),
    ]
    type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label='')

    class Meta:
        model = User
        fields = ['username','email', 'phone', 'password1', 'password2', 'type']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        return cleaned_data

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
