from .models import Project


def projects_normalizer(data):
    result = []
    for project in data:
        project_details = Project.objects.get(pk=project['id'])

        item = {
            'id': project['id'],
            'label': project['label'],
            'description': project['description'],
            'created_at': project['created_at'],
            'updated_at': project['updated_at'],
        }

        result.append(item)

    return result


def project_normalizer(data):
    return {
        'id': data.id,
        'label': data.label,
        'description': data.description,
        'created_at': data.created_at,
        'updated_at': data.updated_at,
    }
