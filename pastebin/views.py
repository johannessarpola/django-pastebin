# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from common.paste_saver import PasteSaver
from pastebin.models import Paste,PasteForm


def index(request):
    latest_texts = Paste.objects.order_by('date')[:5]
    output = ', '.join([q.question_text for q in latest_texts])
    return HttpResponse(output)

def detail(request, text_id):
    return HttpResponse("You're looking at question %s." % text_id)

def results(request, text_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % text_id)

def new_paste(request):
    print(request)
    if(request.method == 'POST'):
        create_paste(request)
        return HttpResponse("ok")
    else:
        return render(request, 'pastebin/new_paste.html', {'form': PasteForm})

def create_paste(request):
    form = PasteForm(request.POST)
    print(form)
    if form.is_valid():
        ps = PasteSaver()
        hash = ps.handle_saving(form, request.user)
    else:
        print("wtf")
