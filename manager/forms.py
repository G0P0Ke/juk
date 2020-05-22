"""
Используемые модули
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import News
from .models import RegManager


class EditProfileForm(forms.ModelForm):
    """
    Форма редактирования профиля
    """
    username = forms.CharField(required=True, label='Логин',)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class CreateNewsForm(forms.ModelForm):
    """
    Форма создания новостей
    """
    class Meta:
        model = News
        fields = ['publicationTitle', 'publicationText']


class RegManagerForm(forms.ModelForm):

    class Meta:
        model = RegManager
        fields = ('fullName', 'userEmail', 'ukEmail', 'appointment', 'date', 'phoneNumber')