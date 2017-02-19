import base64

from django.contrib.auth import authenticate

def basic_auth(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                try:
                    b64dec =  base64.b64decode(auth[1])
                    creds = str(b64dec,'utf-8')
                    uname, passwd = creds.split(':')
                    user = authenticate(username=uname, password=passwd)
                    if user is not None and user.is_active:
                        return True
                except Exception:
                    return False
    else:
        return False