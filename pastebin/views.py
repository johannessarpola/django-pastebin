# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect


from pastebin.models import Paste,PasteForm


def index(request):
    latest_texts = Paste.objects.order_by('date')[:5]
    output = ', '.join([q.question_text for q in latest_texts])
    return HttpResponse(output)

def detail(request, paste_hash):
    from common.paste_retriever import PasteRetriever

    # TODO This needs to check if paste is expired, if it is redirect to 404 or something
    retriever = PasteRetriever()
    p = retriever.find_by("hash", "=", paste_hash) # Not working currently
    paste = retriever.get_by_hash_simplejson(paste_hash)
    return JsonResponse(paste)

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

def remove(request): # TODO Remove this
    from common.paste_remover import PasteRemover
    PasteRemover().removeExpiredPastes()
    return HttpResponse("ok")

def create_paste(request):
    from common.paste_saver import PasteSaver
    form = PasteForm(request.POST)
    if form.is_valid():
        ps = PasteSaver()
        hash = ps.handle_saving(form, request.user)
        return hash
    else:
        print("couldn't save anything")
        return ""