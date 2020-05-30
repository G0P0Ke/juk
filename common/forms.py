"""
Модули, используемые в формах
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Feedback


class LoginForm(forms.Form):
    """
    Форма авторизации
    """
    login = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput, max_length=20)


class SignUpForm(UserCreationForm):
    """
    Форма регистрации
    """
    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ('yourmail', 'title', 'text',)


