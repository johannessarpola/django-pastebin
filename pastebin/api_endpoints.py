from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_paste_body(request):
    import pastebin.core.rest_api_utils as rau
    body = rau.get_request_body_as_dict(request=request)
    return get_paste_params(request=request, paste_hash=body['paste_hash'])

@csrf_exempt
def get_paste_params(request, paste_hash):
    if (request.method == 'POST'):
        """
        Gets the paste and uses basic auth for authentication
        :param request:
        :param paste_hash:
        :return:
        """
        from pastebin.core.paste_retriever import PasteRetriever
        from django.http import JsonResponse
        import pastebin.core.auth
        if request.user.is_authenticated() or pastebin.core.auth.basic_auth(request):
            retriever = PasteRetriever()
            paste_json = retriever.get_by_hash_simplejson(hash=paste_hash)
            if paste_json['expired'] == True or paste_json is None:
                return invalid_or_expired()
            else:
                return JsonResponse(paste_json)
        else:
            return no_login()
    else:
        return HttpResponseBadRequest()

@csrf_exempt
def get_shortened_url_body(request):
    from pastebin.core import rest_api_utils as util
    body = util.get_request_body_as_dict(request=request)
    return get_shortened_url_params(request=request, url=body['url'])

@csrf_exempt
def get_shortened_url_params(request, url):
    """
    generates shortened urls for requested ones
    :param request:
    :param url:
    :return:
    """
    if (request.method == 'POST'):
        import pastebin.core.auth
        if request.user.is_authenticated() or pastebin.core.auth.basic_auth(request):
                from common.url_shortener import GoogleUrlShortener
                gus = GoogleUrlShortener()
                shortened_json = gus.create_shortened_url_json(url=url)
                from django.http import JsonResponse
                if shortened_json is not None:
                    return JsonResponse(shortened_json)
                else:
                    return problem_in_shortening()
        else:
            return no_login()
    else:
        return HttpResponseBadRequest()


def no_login():
    err_ret = {}
    err_ret["message"] = "Could not authenticate user"
    from django.http import JsonResponse
    return JsonResponse(err_ret)

def problem_in_shortening():
    err_ret = {}
    err_ret["message"] = "Url shortening failed"
    from django.http import JsonResponse
    return JsonResponse(err_ret)

def invalid_or_expired():
    err_ret = {}
    err_ret["message"] = "Invalid or expired hash requested"
    from django.http import JsonResponse
    return JsonResponse(err_ret)