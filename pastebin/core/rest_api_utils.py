

def get_request_body_as_dict(request):
    """
    Expects UTF-8
    :param request:
    :return:
    """
    import json as j
    try:
        b_e = request.body.decode('utf-8')
        b = j.loads(b_e)
        return b
    except Exception as e:
        return None

