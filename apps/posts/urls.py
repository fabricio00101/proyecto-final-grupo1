from django.urls import path
from .views import (
    listar_publicaciones, detalle_publicacion, 
    PublicacionCreateView, PublicacionUpdateView, PublicacionDeleteView,
    ComentarioCreateView, ComentarioUpdateView, ComentarioDeleteView
)


app_name = 'publicaciones'

urlpatterns = [
    # Cuando alguien entre a /publicaciones/ verá la lista
    path('', listar_publicaciones, name='listar'),
    path('detalle/<int:id>/', detalle_publicacion, name='detalle'),
    
    # CRUD Publicación
    path('nueva/', PublicacionCreateView.as_view(), name='crear'),
    path('editar/<int:id>/', PublicacionUpdateView.as_view(), name='editar'),
    path('eliminar/<int:id>/', PublicacionDeleteView.as_view(), name='eliminar'),

    # CRUD Comentario
    path('detalle/<int:id>/comentar/', ComentarioCreateView.as_view(), name='comentario_crear'),
    path('comentario/editar/<int:id>/', ComentarioUpdateView.as_view(), name='comentario_editar'),
    path('comentario/eliminar/<int:id>/', ComentarioDeleteView.as_view(), name='comentario_eliminar'),

]

