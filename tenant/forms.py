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
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'username')


class PhotoUpload(forms.Form):
    photo = forms.ImageField()


class ManagerRequestForm(forms.Form):
    inn_company = forms.IntegerField(label='Выберете вашу компанию по ИНН', )


class AppendCompany(forms.Form):
    inn_company = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    company_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    company_ya_num = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
