# Create your views here.
import logging

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect

from pastebin.models import Paste, PasteForm

logger = logging.getLogger(__name__)

def login(request):
    username = request.POST.get('username', 'None')
    password = request.POST.get('password', 'None')
    user = authenticate(username=username, password=password)
    if user is not None:
        return render(request, 'pastebin/index.html') # this can be either e.g redirect
    else:
        from django.contrib.auth.forms import AuthenticationForm
        return render(request, 'pastebin/login.html',  {'form': AuthenticationForm})

def logout(request):
    print("wazza")
    return render(request, 'pastebin/logged_out.html')

def index(request):
    return render(request, 'pastebin/index.html')

def detail(request, paste_hash):
    from pastebin.core.paste_retriever import PasteRetriever
    retriever = PasteRetriever()
    paste_json = retriever.get_by_hash_simplejson(paste_hash)
    if(paste_json['expired'] == True or paste_json is None):
        request.session['hash'] = paste_hash
        return redirect('invalid_hash')
    else:
        return JsonResponse(paste_json)

def invalid_hash(request):
    hash = request.session['hash']
    return HttpResponse("Couldn't find paste with id: {}".format(hash))

def results(request, text_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % text_id)

def new_paste(request):
    if(request.method == 'POST'):
        hash = create_paste(request)
        return redirect('detail', paste_hash=hash)
    else:
        return render(request, 'pastebin/new.html', {'form': PasteForm})

def about(request):
    render(request, 'pastebin/about.html')

def register_user(request):
    from django.contrib.auth.forms import UserCreationForm
    if (request.method == 'POST' ):
        from pastebin.core.user_saver import UserSaver
        from django.contrib.auth import login
        user_saver = UserSaver()
        user = user_saver.handle_saving(request)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("error") # TODO I guess this should redirect to somewhere
    else:
        return render(request, 'pastebin/register.html', {'form': UserCreationForm})

def forgot_password(request):
    if (request.method == 'POST' ):
        return HttpResponse()
    else:
        from django.contrib.auth.forms import PasswordResetForm
        return render(request, 'pastebin/forgot_password.html', {'form': PasswordResetForm})


def create_paste(request):
    from pastebin.core.paste_saver import PasteSaver
    from django.contrib.auth.models import User
    user = User.objects.get(id=1) # TODO This needs to come from session store or something similar
    form = PasteForm(request.POST)
    if form.is_valid():
        ps = PasteSaver()
        hash = ps.handle_saving(form, user)
        return hash
    else:
        logger.warning("Received invalid form: {}".format(str(form)))
        return "" # TODO Meh