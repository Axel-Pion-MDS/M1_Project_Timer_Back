from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'label',
            'description',
            'provisional_start',
            'provisional_end',
            'provisional_time',
            'is_billable',
            'is_ended',
            # 'project',
        )
