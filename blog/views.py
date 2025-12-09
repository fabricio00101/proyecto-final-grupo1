from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
def Acerca_de(request):
    return render(request, 'Acerca_de.html')
