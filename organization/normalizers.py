from project.models import Project
from team.models import Team


def organizations_normalizer(data):
    result = []
    for organization in data:
        project_details = Project.objects.filter(organization=organization['id']).all()
        team_details = Team.objects.filter(organization=organization['id']).all()

        projects = []
        for project in project_details:
            item = {
                'id': project.id,
                'label': project.label,
            }

            projects.append(item)

        teams = []
        for team in team_details:
            item = {
                'id': team.id,
                'label': team.label
            }

            teams.append(item)

        item = {
            'id': organization['id'],
            'label': organization['label'],
            'description': organization['description'],
            'created_at': organization['created_at'],
            'updated_at': organization['updated_at'],
            'teams': teams if teams else 'null',
            'projects': projects if projects else 'null'
        }

        result.append(item)

    return result


def organization_normalizer(data):
    project_details = Project.objects.filter(organization=data.id).all()
    team_details = Team.objects.filter(organization=data.id).all()

    projects = []
    for project in project_details:
        item = {
            'id': project.id,
            'label': project.label,
        }

        projects.append(item)

    teams = []
    for team in team_details:
        item = {
            'id': team.id,
            'label': team.label
        }

        teams.append(item)

    return {
        'id': data.id,
        'label': data.label,
        'description': data.description,
        'created_at': data.created_at,
        'updated_at': data.updated_at,
        'teams': teams if teams else 'null',
        'projects': projects if projects else 'null'
    }
