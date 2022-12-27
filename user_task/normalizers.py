from .models import UserTask


def user_tasks_normalizer(data):
    result = []
    for user_task in data:
        user_task_details = UserTask.objects.get(pk=user_task.id)

        item = {
            'id': user_task.id,
            'task': {
                'id': user_task_details.task.id,
                'label': user_task_details.task.label,
            },
            'user': {
                'id': user_task_details.user.id,
                'firstname': user_task_details.user.firstname,
                'lastname': user_task_details.user.lastname,
                'email': user_task_details.user.email,
            }
        }

        result.append(item)

    return result


def user_task_normalizer(data):
    members = []
    users_in_task = UserTask.objects.filter(task=data.task.id)

    for member in users_in_task:
        members.append({
            'id': member.user.id,
            'firstname': member.user.firstname,
            'lastname': member.user.lastname,
            'email': member.user.email,
        })

    return {
        'id': data.id,
        'task': {
            'id': data.task.id,
            'label': data.task.label,
        },
        'user': members if members else 'null'
    }


def users_from_task_normalizer(data, task):
    result = [{
        'task': {
            'id': task.id,
            'label': task.label,
        }
    }]

    items = []
    for user in data:
        items.append({
            'id': user.user.id,
            'firstname': user.user.firstname,
            'lastname': user.user.lastname,
            'email': user.user.email,
        })

    result.append({
        'users': items if items else 'null'
    })

    return result
