from django.shortcuts import render
from .models import Post

# Create your views here.

# Esta función busca los posts en la base de datos y los manda al HTML
def listar_posts(request):
    # Busca todos los posts
    posts = Post.objects.all()
    # Renderizamos el html y le enviamos la lista de posts
    return render(request, 'lista_post.html', {'posts': posts})