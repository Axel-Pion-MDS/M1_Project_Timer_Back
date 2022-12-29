from .models import TaskTimer

def task_timers_normalizer(data):
    result = []
    for task_timer in data:
        task_timer_details = TaskTimer.objects.get(pk=task_timer['id'])

        item = {
            'id': task_timer['id'],
            'start_time': task_timer['start_time'],
            'end_time': task_timer['end_time'],
            'total_time': task_timer['total_time'],
            'task': {
                'id': task_timer_details.task.id,
                'label': task_timer_details.task.label,
                'description': task_timer_details.task.description,
            } if task_timer_details.task else 'null'
        }

        result.append(item)

    return result

def task_timer_normalizer(data):
    return {
        'id': data.id,
        'start_time': data.start_time,
        'end_time': data.end_time,
        'total_time': data.total_time,
        'task': {
            'id': data.task.id,
            'label': data.task.label,
            'description': data.task.description,
        } if data.task else 'null'
    }

