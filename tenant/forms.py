"""
Используемые модули
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class EditProfileForm(forms.ModelForm):
    """
    Форма изменения профиля
    """
    username = forms.CharField(required=True, label='Логин',)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class PhotoUpload(forms.Form):
    photo = forms.ImageField()


class ManagerRequestForm(forms.Form):
    inn_company = forms.IntegerField(label='Выберете вашу компанию по ИНН', )


class AppendCompany(forms.Form):
    inn_company = forms.IntegerField()
    company_name = forms.CharField(required=True)