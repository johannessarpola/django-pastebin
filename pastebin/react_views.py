from django.shortcuts import render


def about(request):
    return render(request, 'pastebin/react_hello.html')

