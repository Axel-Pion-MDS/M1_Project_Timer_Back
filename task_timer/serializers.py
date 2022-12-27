from rest_framework import serializers
from .models import TaskTimer 
from .models import Task 

class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = ['id', 'label']


class TaskTimerSerializer(serializers.ModelSerializer):
  class Meta:
    model = TaskTimer
    fields = ['id','task' 'start_time', 'end_time', 'elapsed_time', 'paused']