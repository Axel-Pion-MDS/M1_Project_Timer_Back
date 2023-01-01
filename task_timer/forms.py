from django import forms
from .models import TaskTimer


class TaskTimerForm(forms.ModelForm):
    class Meta:
        model = TaskTimer
        fields = (
            'start_time',
            'end_time',
            'total_time',
            'task'
        )
