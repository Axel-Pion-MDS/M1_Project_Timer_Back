from django.http import JsonResponse
from django.conf import settings


def send_json_response(code='SUCCES', result='', data={}):
    """Send response in JSON format. The response is returned with code, result and data.

    Args:
        result (str, optional): Response message. Defaults to ''
        code (int, optional): Response status code. Defaults to 'SUCCESS'.
        data (dict, optional): Reponse data. Defaults to {}.
    """

    if not code in list(settings.HTTP_CONSTANTS.keys()):
        print('code is not in responses list')
        code = list(settings.HTTP_CONSTANTS.keys())[0]

    if not result:
        result = code.lower()

    return JsonResponse({'code': settings.HTTP_CONSTANTS[code], 'result': result, 'data': data})
