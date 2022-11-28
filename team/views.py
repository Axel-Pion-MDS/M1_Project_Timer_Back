import json
from services.verify_method import request_method_is
from services.errors import Errors
from services.send_response import send_json_response
from team.normalizers import teams_normalizer, team_normalizer
from team.models import Team
from team.forms import TeamForm

def get_teams(request):
    errors = Errors()
    
    # request method must be GET type
    if not request_method_is(request, 'GET'):    
        errors.add(0, 'method', 'Must be a GET method')
        return send_json_response('NOT_ALLOWED', 'Not Allowed', {**errors.get_dict_erros()})

    teams = teams_normalizer(Team.objects.all())
    return send_json_response('SUCCESS', 'success', teams)

def get_team(request, team_id):
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