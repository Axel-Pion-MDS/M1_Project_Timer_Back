from django.db import models


class Role(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return '{}. {}'.format(self.id, self.label)
