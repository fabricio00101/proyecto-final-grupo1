from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import RegistroForm

# Create your views here.

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            # Logueamos al usuario automáticamente después de registrarse
            login(request, usuario)
            return redirect('index')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})
