from django.shortcuts import render, get_object_or_404
from .models import Post, Categoria

# Create your views here.

# Esta función busca los posts en la base de datos y los manda al HTML
def listar_posts(request):
    # Busca todos los posts
    posts = Post.objects.all()

    # Sistema de filtrado por categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        posts = posts.filter(categoria_id=categoria_id)

    # Sistema de ordenamiento
    orden = request.GET.get('orden')
    if orden == 'antiguo':
        posts = posts.order_by('publicado') #Acendente
    elif orden == 'alfabetico':
        posts = posts.order_by('titulo') # A-Z
    elif orden == 'alfabetico_inv':
        posts = posts.order_by('-titulo') # Z-A
    else:
        posts = posts.order_by('-publicado') #Por defecto: Recientes primero

    categorias = Categoria.objects.all()

    contexto = {
        'posts': posts,
        'categorias': categorias,
    }
    return render(request, 'lista_posts.html', contexto)


def post_detalle(request, id):
    post = get_object_or_404(Post, id=id)
    contexto={
        'post': post
    }
    return render(request, 'post_detalle.html', contexto)
