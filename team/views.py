from services.verify_method import request_method_is
from services.errors import Errors
from services.send_response import send_json_response
from team.normalizers import teams_normalizer, team_normalizer
from team.models import Team

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
    print(team_id)
    if not Team.objects.filter(pk=team_id).exists():
        errors.add(0, 'id', 'Team with id: {} not found'.format(team_id))
        return send_json_response('NOT_FOUND', 'Not Found', {**errors.get_dict_erros()})

    team = team_normalizer(Team.objects.get(pk=team_id))
    return send_json_response('SUCCESS', 'success', team)