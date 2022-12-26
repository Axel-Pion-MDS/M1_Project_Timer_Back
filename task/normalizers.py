from project.models import Project
from .models import Task


def tasks_normalizer(data):
    result = []
    for task in data:
        item = {
            'id': task.id,
            'label': task.label,
            'description': task.description,
            'provisional_start': task.provisional_start,
            'provisional_end': task.provisional_end,
            'provisional_time': task.provisional_time,
            'is_billable': task.is_billable,
            'is_ended': task.is_ended,
            'project': {
                'id': task.project.id,
                'label': task.project.label,
            },
            'created_at': task.created_at,
            'updated_at': task.updated_at,
        }

        result.append(item)

    return result


def task_normalizer(data):
    return {
        'id': data.id,
        'label': data.label,
        'description': data.description,
        'provisional_start': data.provisional_start,
        'provisional_end': data.provisional_end,
        'provisional_time': data.provisional_time,
        'is_billable': data.is_billable,
        'is_ended': data.is_ended,
        'project': {
            'id': data.project.id,
            'label': data.project.label,
        },
        'created_at': data.created_at,
        'updated_at': data.updated_at,
    }