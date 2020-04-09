from django import forms


class DiscussionCreationForm(forms.Form):
    theme = forms.CharField(max_length=20, required=True, label="Тема")
    category = forms.CharField(max_length=20, required=True, label="Категория")
    description = forms.CharField(max_length=40, required=True, label="Описание")
    anonymous = forms.BooleanField(required=False)

