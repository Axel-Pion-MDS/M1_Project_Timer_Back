from django import forms
from .models import UserOrganization


class UserOrganizationForm(forms.ModelForm):
    class Meta:
        model = UserOrganization
        fields = (
            'user',
            'organization',
            'role',
        )
