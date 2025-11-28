from django.urls import path
from .views import listar_posts, post_detalle

app_name = 'posts'

urlpatterns = [
    # Cuando alguien entre a /posts/ verá la lista
    path('', listar_posts, name = 'listar_posts'),
    path('detalle/<int:id>/', post_detalle, name = 'post_detalle'),
    
]

