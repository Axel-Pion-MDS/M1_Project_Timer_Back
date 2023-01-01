from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'firstname',
            'lastname',
            'email',
            'password'
        )
        widgets = {
            'password': forms.PasswordInput(),
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'password'
        )
        widgets = {
            'password': forms.PasswordInput(),
        }
