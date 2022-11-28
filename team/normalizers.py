from team.models import Team


def teams_normalizer(data):
    return [{
        'id': team.id,
        'label': team.label
    } for team in data]


def team_normalizer(data):
    return {
        'id': data.id,
        'label': data.label,
    }
