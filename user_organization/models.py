from django.db import models
from django.conf import settings


class UserOrganization(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=False)
    role = models.ForeignKey(
        'role.Role',
        on_delete=models.CASCADE,
        null=False,
        blank=True,
        default=settings.ROLES['ROLE_ORGANIZATION_MEMBER']
    )

    def __str__(self):
        return '{}. {} - {} / {} ({})'.format(
            self.pk,
            self.organization.id,
            self.organization.label,
            self.user.email,
            self.role.label
        )
