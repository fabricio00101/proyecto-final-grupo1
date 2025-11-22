from django.urls import path
from .views import listar_posts

app_name = 'posts'

urlpatterns = [
    # Cuando alguien entre a /posts/ verá la lista
    path('', listas_posts, name= 'listar_posts'),
]

