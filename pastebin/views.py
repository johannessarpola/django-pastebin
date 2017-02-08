# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect


from pastebin.models import Paste,PasteForm

import logging
logger = logging.getLogger(__name__)

def index(request):
    latest_texts = Paste.objects.order_by('date')[:5]
    output = ', '.join([q.question_text for q in latest_texts])
    return HttpResponse(output)

def detail(request, paste_hash):
    from common.paste_retriever import PasteRetriever
    retriever = PasteRetriever()
    paste_json = retriever.get_by_hash_simplejson(paste_hash)
    if(paste_json['expired'] == True or paste_json is None):
        from django.http import HttpResponseRedirect
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

def create_paste(request):
    from common.paste_saver import PasteSaver
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