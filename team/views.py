import json
from services.verify_method import request_method_is
from services.errors import Errors
from services.send_response import send_json_response
from team.normalizers import teams_normalizer, team_normalizer, user_team_normalizer
from team.models import Team, UserTeam
from team.forms import TeamForm, UserTeamForm
from role.models import Role
from user.models import User

def get_teams(request):
    """GET list of informations from teams 

    Args:
        request (class): Django request Class

    Returns:
        dict: response with informations from teams
    """
    errors = Errors()
    
    # request method must be GET type
    if not request_method_is(request, 'GET'):    
        errors.add(0, 'method', 'Must be a GET method')
        return send_json_response('NOT_ALLOWED', 'Not Allowed', {**errors.get_dict_erros()})

    teams = teams_normalizer(Team.objects.all())
    return send_json_response('SUCCESS', 'success', teams)


def get_team(request, team_id):
    """GET informations from a team using its id

    Args:
        request (class): Django request Class
        team_id (int): team's id

    Returns:
        dict: response with team's informations
    """
    errors = Errors()
    
    # request method must be GET type
    if not request_method_is(request, 'GET'):    
        errors.add(0, 'method', 'Must be a GET method')
        return send_json_response('NOT_ALLOWED', 'Not Allowed', {**errors.get_dict_erros()})
    
    # check if Team object exists
    if not Team.objects.filter(pk=team_id).exists():
        errors.add(0, 'id', 'Team with id: {} not found'.format(team_id))
        return send_json_response('NOT_FOUND', 'Not Found', {**errors.get_dict_erros()})

    team = team_normalizer(Team.objects.get(pk=team_id))
    return send_json_response('SUCCESS', 'success', team)


def add_team(request):
    """POST new team

    Args:
        request (class): Django request Class

    Returns:
        dict: response with new team's informations
    """
    errors = Errors()
    
    # request method must be POST type
    if not request_method_is(request, 'POST'):    
        errors.add(0, 'method', 'Must be a POST method')
        return send_json_response('NOT_ALLOWED', 'Not Allowed', {**errors.get_dict_erros()})

    content = json.loads(request.body.decode('utf-8'))
    form = TeamForm(content)

    # if form is not valid, display form errors
    if not form.is_valid():
        # loop and append errors from erros.items()
        for form_error in list(form.errors.items()):
            errors.add(0, form_error[0], ', '.join(form_error[1]))
        return send_json_response('INTERNAL_SERVER_ERROR', 'error', {**errors.get_dict_erros()})

    # save and get team object
    team_object = form.save()
    team = team_normalizer(Team.objects.get(pk=team_object.id))
    return send_json_response('SUCCESS', 'success', team)


def update_team(request):
    """PATCH team informations with the id in the body

    Args:
        request (class): Django request Class

    Returns:
        dict: response with new team's informations
    """
    errors = Errors()
    
    # request method must be PATCH type
    if not request_method_is(request, 'PATCH'):    
        errors.add(0, 'method', 'Must be a PATCH method')
        return send_json_response('NOT_ALLOWED', 'Not Allowed', {**errors.get_dict_erros()})

    content = json.loads(request.body.decode('utf-8'))
    team_id = content['id']

    # check if Team object exists
    if not Team.objects.filter(pk=team_id).exists():
        errors.add(0, 'id', 'Team with id: {} not found'.format(team_id))
        return send_json_response('NOT_FOUND', 'Not Found', {**errors.get_dict_erros()})

    team_object = Team.objects.get(pk=team_id)
    form = TeamForm(instance=team_object, data=content)

    # if form is not valid, display form errors
    if not form.is_valid():
        # loop and append errors from erros.items()
        for form_error in list(form.errors.items()):
            errors.add(0, form_error[0], ', '.join(form_error[1]))
        return send_json_response('INTERNAL_SERVER_ERROR', 'error', {**errors.get_dict_erros()})

    # save and get team object
    team_object.save()
    team = team_normalizer(Team.objects.get(pk=team_object.id))
    return send_json_response('SUCCESS', 'success', team)


def delete_team(request, team_id):
    """DELETE a team using the id

    Args:
        request (class): Django request class
        team_id (int): team's id

    Returns:
        json: response
    """
    errors = Errors()
    
    # request method must be DELETE type
    if not request_method_is(request, 'DELETE'):    
        errors.add(0, 'method', 'Must be a DELETE method')
        return send_json_response('NOT_ALLOWED', 'Not Allowed', {**errors.get_dict_erros()})

    # check if Team object exists
    if not Team.objects.filter(pk=team_id).exists():
        errors.add(0, 'id', 'Team with id: {} not found'.format(team_id))
        return send_json_response('NOT_FOUND', 'Not Found', {**errors.get_dict_erros()})

    Team.objects.get(pk=team_id).delete()
    return send_json_response('SUCCESS', 'success', [])


def add_user_team(request):
    errors = Errors()
    
    # request method must be POST type
    if not request_method_is(request, 'POST'):    
        errors.add(0, 'method', 'Must be a POST method')
        return send_json_response('NOT_ALLOWED', 'Not Allowed', {**errors.get_dict_erros()})

    content = json.loads(request.body.decode('utf-8'))
    team_id = content['team_id']
    user_id = content['user_id']
    role_id = content['role_id']

    # check if Team object exists
    if not Team.objects.filter(pk=team_id).exists():
        errors.add(0, 'team_id', 'Team with id: {} not found'.format(team_id))
    # check if User object exists
    if not User.objects.filter(pk=user_id).exists():
        errors.add(0, 'user_id', 'User with id: {} not found'.format(user_id))
    # check if Role object exists
    if not Role.objects.filter(pk=role_id).exists():
        errors.add(0, 'role_id', 'Role with id: {} not found'.format(role_id))
    
    # if Error has errors return response with all errors 
    if errors.has_errors():
        return send_json_response('NOT_FOUND', 'Not Found', {**errors.get_dict_erros()})
    
    # retrieve Team, User and Role
    team = Team.objects.get(pk=team_id)
    user = User.objects.get(pk=user_id)
    role = Role.objects.get(pk=role_id)

    # check if UserTeam object not exists
    if UserTeam.objects.filter(user=user, team=team).exists():
        errors.add(0, 'user', 'This user already exists in this team')
        return send_json_response('NOT_FOUND', 'Not Found', {**errors.get_dict_erros()})        

    form = UserTeamForm({
        'team': team,
        'user': user,
        'role': role
    })

    # if form is not valid, display form errors
    if not form.is_valid():
        # loop and append errors from erros.items()
        for form_error in list(form.errors.items()):
            errors.add(0, form_error[0], ', '.join(form_error[1]))
        return send_json_response('INTERNAL_SERVER_ERROR', 'error', {**errors.get_dict_erros()})

    # save and get team object
    user_team_object = form.save()
    user_team = user_team_normalizer(UserTeam.objects.get(pk=user_team_object.id))
    return send_json_response('SUCCESS', 'success', user_team)