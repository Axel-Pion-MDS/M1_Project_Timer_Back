from django.db import models
from django.conf import settings


class Team(models.Model):
    label = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=512, default='')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    organization = models.ForeignKey('organization.Organization', on_delete=models.PROTECT, null=True, default=None)

    def __str__(self):
        return '{}. {} from organization {}'.format(
            self.id,
            self.label,
            self.organization
        )

    def get_users(self):
        return [user_team 
            for user_team in UserTeam.objects.filter(team=self).all()]


class UserTeam(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.PROTECT, null=False)
    team = models.ForeignKey('team.Team', on_delete=models.PROTECT, null=False)
    role = models.ForeignKey('role.Role', on_delete=models.PROTECT, null=False, default=settings.ROLES['ROLE_USER'])
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return '{}. user ({}) in team({})'.format(
            self.id,
            self.user,
            self.team
        )