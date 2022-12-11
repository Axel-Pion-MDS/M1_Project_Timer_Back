from django import forms
from team.models import Team, UserTeam


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = (
            'label',
            'description',
            'organization'
        )

class UserTeamForm(forms.ModelForm):
    class Meta:
        model = UserTeam
        fields = {
            'user',
            'team',
            'role'
        }