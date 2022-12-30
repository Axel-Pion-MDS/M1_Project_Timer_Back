from django.db import models

class TaskTimer(models.Model):
  start_time = models.DateTimeField(null=True)
  end_time = models.DateTimeField(null=True)
  total_time = models.DurationField(null=True, blank=True)
  task = models.ForeignKey('task.Task', on_delete=models.CASCADE, null=False,default=None)

  def __str__(self):
    return '{}. {}'.format(self.pk, self.start_time, self.end_time, self.total_time,self.task)