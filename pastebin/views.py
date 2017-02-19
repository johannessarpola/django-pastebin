# Create your views here.
import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from pastebin.forms.paste_forms import PasteForm

logger = logging.getLogger(__name__)


def login_view(request):
    username = request.POST.get('username', 'None')
    password = request.POST.get('password', 'None')
    user = authenticate(username=username, password=password)
    if user is not None and user.is_authenticated():  # render(request, 'pastebin/index.html')
        login(request, user)
        return redirect('index')  # this can be either e.g redirect
    else:
        from django.contrib.auth.forms import AuthenticationForm
        return render(request, 'pastebin/login.html', {'form': AuthenticationForm})

@login_required
def index(request):
    from pastebin.core.paste_retriever import PasteRetriever
    import pastebin.core.paste_utils as util
    excerpt_length = 15  # TODO Store in config
    pastes = PasteRetriever().get_lastest_5()
    pastes = util.create_excerpts_for_text_fields(pastes=pastes, excerpt_length=excerpt_length)
    return render(request, 'pastebin/index.html', {'latest': pastes})

@login_required
def view_paste(request, paste_hash):
    paste = retrieve_paste(paste_hash)
    if paste is None or paste.is_expired():
        request.session['hash'] = paste_hash
        return redirect('invalid_hash')
    else:
        return render(request, 'pastebin/paste.html', {'paste': paste})


def invalid_hash(request):
    hash = request.session['hash']
    return HttpResponse("Couldn't find paste with id: {}".format(hash))

@login_required
def new_paste(request):
    if (request.method == 'POST'):
        from pastebin.core import paste_saver
        hash = paste_saver.paste_from_request(request)
        if hash is not None:
            return redirect('view', paste_hash=hash)
        else:
            from django.contrib import messages
            logger.warning("Couldn't save form from request: {}".format(request))
            messages.add_message(request, messages.ERROR, 'There was problem saving the form!')
            return render(request, 'pastebin/new.html', {'form': PasteForm})
    else:
        return render(request, 'pastebin/new.html', {'form': PasteForm})


def about(request):
    return render(request, 'pastebin/about.html')


def register_user(request):
    from django.contrib.auth.forms import UserCreationForm
    if (request.method == 'POST'):
        from pastebin.core.user_saver import UserSaver
        from django.contrib.auth import login
        user_saver = UserSaver()
        user = user_saver.handle_saving(request)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("error")  # TODO I guess this should redirect to somewhere
    else:
        from pastebin.forms.user_forms import RegistrationForm
        return render(request, 'pastebin/register.html', {'form': RegistrationForm})


def forgot_password(request):
    if (request.method == 'POST'):
        return HttpResponse()  # FIXME Reset password
    else:
        from django.contrib.auth.forms import PasswordResetForm
        return render(request, 'pastebin/forgot_password.html', {'form': PasswordResetForm})

@login_required
def me(request):
    from django.contrib.auth.forms import PasswordResetForm
    from pastebin.core.user_retriever import UserRetriever
    e_info = UserRetriever().get_user_extra_info_if_exists(request.user)
    return render(request, 'pastebin/profile.html', {'extra_info': e_info})


def logout(request):
    from django.contrib.auth.forms import AuthenticationForm
    from django.contrib.auth import logout
    from django.contrib import messages
    logout(request)
    messages.add_message(request, messages.INFO, 'Logged out successfully!')
    return render(request, 'pastebin/login.html', {'form': AuthenticationForm})

def retrieve_paste(paste_hash):
    # TODO Find a correct place for this too
    from pastebin.core.paste_retriever import PasteRetriever
    retriever = PasteRetriever()
    paste = retriever.get_by_hash(paste_hash)
    return paste

@login_required
def edit_profile(request):
    if (request.method == 'POST'):
        # TODO Save edits
        return None
    else:
        import pastebin.forms.user_forms as forms
        e_edit_form = forms.create_user_extra_edit_form_with_initial(request.user)
        u_edit_form = forms.create_user_edit_form_with_initial(request.user)
        return render(request, 'pastebin/edit_profile.html', {'forms': [e_edit_form, u_edit_form]})
