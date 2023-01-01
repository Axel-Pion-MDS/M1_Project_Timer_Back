from team.models import Team, UserTeam


def users_teams_normalizer(data):
    return [{
        'id': user_team.id,
        'user': user_team.user.id,
        'team': user_team.team.id,
        'role': {
            'id': user_team.role.id,
            'label': user_team.role.label
        }
    } for user_team in data]


def user_team_normalizer(data):
    return {
        'id': data.id,
        'user': data.user.id,
        'team': data.team.id,
        'role': {
            'id': data.role.id,
            'label': data.role.label
        }
    }


def teams_normalizer(data):
    return [{
        'id': team.id,
        'label': team.label,
        'description': team.description,
        'organization': {
            'id': team.organization.id,
            'label': team.organization.label
        },
        'users': users_teams_normalizer(team.get_users()),
        'created_at': team.created_at,
        'updated_at': team.updated_at
    } for team in data]


def team_normalizer(data):
    return {
        'id': data.id,
        'label': data.label,
        'description': data.description,
        'organization': {
            'id': data.organization.id,
            'label': data.organization.label
        },
        'users': users_teams_normalizer(data.get_users()),
        'created_at': data.created_at,
        'updated_at': data.updated_at
    }