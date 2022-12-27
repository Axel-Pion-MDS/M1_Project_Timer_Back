from rest_framework import serializers
from .models import Task 

class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = ('id', 'label', 'start_time', 'end_time', 'elapsed_time', 'paused','created_at','updated_at')