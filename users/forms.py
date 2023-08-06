from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import User


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class CodeForm(forms.Form):
    code = forms.IntegerField(
        label='Введите код',
        widget=forms.TextInput(attrs={'class': 'form-control input-lg'})
    )

    class Meta:
        fields = ('code',)