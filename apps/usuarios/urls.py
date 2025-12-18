from django.urls import path
from .views import registro, contacto

app_name = 'usuarios'

urlpatterns = [
    path('registrarse/', registro, name='registrarse'),
    path('contacto/', contacto, name='contacto'),
]
