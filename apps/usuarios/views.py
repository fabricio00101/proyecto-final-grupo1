from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import RegistroForm
from .forms_contacto import ContactoForm
from django.core.mail import send_mail
from django.conf import settings
# Vista de contacto
def contacto(request):
    enviado = False
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']
            # Enviar email (opcional, requiere configuración SMTP)
            # send_mail(
            #     f'Contacto de {nombre}',
            #     mensaje,
            #     email,
            #     [settings.DEFAULT_FROM_EMAIL],
            # )
            enviado = True
    else:
        form = ContactoForm()
    return render(request, 'usuarios/contacto.html', {'form': form, 'enviado': enviado})

# Create your views here.

def registro(request):
    if request.user.is_authenticated:
        return redirect('index')
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
