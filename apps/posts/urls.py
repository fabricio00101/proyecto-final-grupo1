from django.urls import path
from .views import (
    listar_posts, post_detalle, 
    PostCreateView, PostUpdateView, PostDeleteView,
    ComentarioCreateView, ComentarioUpdateView, ComentarioDeleteView
)


app_name = 'posts'

urlpatterns = [
    # Cuando alguien entre a /posts/ verá la lista
    path('', listar_posts, name = 'listar_posts'),
    path('detalle/<int:id>/', post_detalle, name = 'post_detalle'),
    
    # CRUD Post
    path('nuevo/', PostCreateView.as_view(), name='post_create'),
    path('editar/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('eliminar/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),

    # CRUD Comentario
    path('detalle/<int:pk>/comentar/', ComentarioCreateView.as_view(), name='comentario_create'),
    path('comentario/editar/<int:pk>/', ComentarioUpdateView.as_view(), name='comentario_update'),
    path('comentario/eliminar/<int:pk>/', ComentarioDeleteView.as_view(), name='comentario_delete'),

]

