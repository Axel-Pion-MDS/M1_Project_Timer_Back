from django.db import models

class TaskTimer(models.Model):
  task = models.ForeignKey('task.task', on_delete=models.CASCADE)
  start_time = models.DateTimeField(null=True)
  end_time = models.DateTimeField(null=True)
  total_time = models.DurationField(null=True, blank=True)