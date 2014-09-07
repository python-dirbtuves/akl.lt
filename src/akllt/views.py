from django.shortcuts import render


def index(request):
    return render(request, 'base.html')

def apie(request):
    return render(request, 'apie.html')

def naujienos(request):
    return render(request, 'naujienos.html')

def nuorodos(request):
    return render(request, 'nuorodos.html')

def programos(request):
    return render(request, 'programos.html')

def wiki(request):
    return render(request, 'wiki.html')

def atviras_kodas(request):
    return render(request, 'atviras_kodas.html')


