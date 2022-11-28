from team.models import Team


def teams_normalizer(data):
    return [{
        'id': team.id,
        'label': team.label,
        'description': team.description,
        # 'organization': team.organization.id
    } for team in data]


def team_normalizer(data):
    return {
        'id': data.id,
        'label': data.label,
        'description': data.description,
        # 'organization': team.organization.id
    }
