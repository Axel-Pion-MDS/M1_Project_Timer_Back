from django.db import models


class Project(models.Model):
    label = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        blank=False, null=False,
        default=None
    )
    team = models.ForeignKey('team.Team', on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return '{}. {} - created on {}, updated on {}'.format(self.pk, self.label, self.created_at, self.updated_at)
