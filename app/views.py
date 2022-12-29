from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from service.send_response import send_json_response
from service.verify_method import request_method_is
from service.errors import Errors


@csrf_exempt
def send_csrf_token(request):
    """Send CSRF token to user

    Args:
        request (class): Django request
    """
    errors = Errors()

    # request method must be POST
    if not request_method_is(request, 'POST'):
        errors.add(1, 'method', 'Must be a POST method')
        return send_json_response('NOT_ALLOWED', 'Not Allowed', {**errors.get_dict_erros()})

    return send_json_response('SUCCESS', 'success', {'csrf_token': csrf.get_token(request)})
