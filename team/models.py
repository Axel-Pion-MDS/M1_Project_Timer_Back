from django.db import models


class Team(models.Model):
    label = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=512, default='')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    # organization = models.ForeignKey('organization.Organization', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return '{}. {} form organization {}'.format(
            self.id,
            self.label,
            '' #self.organization.label
        )