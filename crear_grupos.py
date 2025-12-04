import os
import django
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.configuraciones.local')
django.setup()


from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.posts.models import Post, Comentario

def crear_grupos():
    # Crear grupos
    visitante, _ = Group.objects.get_or_create(name='Visitante')
    miembro, _ = Group.objects.get_or_create(name='Miembro')
    colaborador, _ = Group.objects.get_or_create(name='Colaborador')

    # Permisos para Colaborador
    ct_post = ContentType.objects.get_for_model(Post)
    ct_comentario = ContentType.objects.get_for_model(Comentario)
    
    permisos_colaborador = Permission.objects.filter(content_type__in=[ct_post, ct_comentario])
    colaborador.permissions.set(permisos_colaborador)

    # Permisos para Miembro (solo comentarios)
    # En realidad, la lógica de "solo sus propios comentarios" se maneja en las vistas/templates,
    # pero podemos dar permiso básico de añadir comentario.
    permiso_add_comentario = Permission.objects.get(codename='add_comentario', content_type=ct_comentario)
    miembro.permissions.add(permiso_add_comentario)

    print("Grupos y permisos creados exitosamente.")

if __name__ == '__main__':
    crear_grupos()

