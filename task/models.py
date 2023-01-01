from django.db import models


class Task(models.Model):
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    provisional_start = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    provisional_end = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    provisional_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    is_billable = models.BooleanField()
    is_ended = models.BooleanField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '{}. {}'.format(self.id, self.label)
