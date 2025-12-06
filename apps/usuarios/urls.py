from django.urls import path
from .views import registro

app_name = 'usuarios'

urlpatterns = [
    path('registrarse/', registro, name='registrarse')
]
