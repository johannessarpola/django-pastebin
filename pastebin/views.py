# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from common.paste_saver import PasteSaver
from pastebin.models import Paste,PasteForm


def index(request):
    latest_texts = Paste.objects.order_by('date')[:5]
    output = ', '.join([q.question_text for q in latest_texts])
    return HttpResponse(output)

def detail(request, paste_hash):
    return HttpResponse("You're looking at question %s." % paste_hash)

def results(request, text_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % text_id)

def new_paste(request):
    if(request.method == 'POST'):
        hash = create_paste(request)
        return redirect('detail', paste_hash=hash)
    else:
        return render(request, 'pastebin/new_paste.html', {'form': PasteForm})

def create_paste(request):
    form = PasteForm(request.POST)
    if form.is_valid():
        ps = PasteSaver()
        hash = ps.handle_saving(form, request.user)
        return hash
    else:
        print("couldn't save anything")
        return ""