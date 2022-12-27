from django.db import models

class TaskTimer(models.Model):
  # task = models.ForeignKey('task.task', on_delete=models.CASCADE)
  start_time = models.DateTimeField(null=True)
  end_time = models.DateTimeField(null=True)
  total_time = models.DurationField(null=True, blank=True)

  def __str__(self):
    return '{}. {} - created on {}, updated on {}'.format(self.pk, self.start_time, self.end_time, self.total_time)