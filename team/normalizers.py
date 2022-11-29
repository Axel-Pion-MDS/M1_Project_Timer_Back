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


def teams_normalizer(data):
    return [{
        'id': team.id,
        'label': team.label,
        'description': team.description,
        # 'organization': team.organization.id,
        'users': users_teams_normalizer(team.get_users()),
        'created_at': team.created_at,
        'updated_at': team.updated_at
    } for team in data]


def team_normalizer(data):
    return {
        'id': data.id,
        'label': data.label,
        'description': data.description,
        # 'organization': team.organization.id,
        'users': users_teams_normalizer(data.get_users()),
        'created_at': data.created_at,
        'updated_at': data.updated_at
    }