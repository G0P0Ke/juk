from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(required=True, label='Логин',)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False, label='Имя',)
    last_name = forms.CharField(required=False, label='Фамилия',)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')