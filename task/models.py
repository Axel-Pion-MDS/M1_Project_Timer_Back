from django.db import models

class Task(models.Model):
  label = models.CharField(max_length=100)
  description = models.CharField(max_length=255)
  start_time = models.DateTimeField(null=True)
  end_time = models.DateTimeField(null=True)
  elapsed_time = models.DurationField(null=True)
  paused = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

  