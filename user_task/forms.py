from django import forms
from .models import UserTask


class UserTaskForm(forms.ModelForm):
    class Meta:
        model = UserTask
        fields = (
            'user',
            'task',
        )
