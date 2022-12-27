from django.db import models


class Organization(models.Model):
    label = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return '{}. {} - created on {}, updated on {}'.format(self.pk, self.label, self.created_at, self.updated_at)
