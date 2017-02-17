def detail(request, paste_hash):
    from pastebin.core.paste_retriever import PasteRetriever
    from django.http import JsonResponse
    retriever = PasteRetriever()
    paste_json = retriever.get_by_hash_simplejson(paste_hash)
    if(paste_json['expired'] == True or paste_json is None):
        err_ret = dict()
        err_ret["message"] = "Invalid or expired hash requested"
        return JsonResponse(err_ret)
    else:
        return JsonResponse(paste_json)