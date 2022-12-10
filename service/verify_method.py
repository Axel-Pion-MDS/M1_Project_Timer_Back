def request_method_is(request, type):
    """Checks if request method is desired

    Args:
        request (class): Django request
        type (str): Method desired

    Returns:
        boolean: True if request method is desired
    """

    must_type = type.lower()
    request_type = request.method.lower()

    if request_type == must_type:
        return True
    return False
