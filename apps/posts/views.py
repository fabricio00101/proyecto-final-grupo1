from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Categoria, Comentario
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

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
    comentarios = post.comentarios.all()
    contexto={
        'post': post,
        'comentarios': comentarios
    }
    return render(request, 'post_detalle.html', contexto)

# Vistas para Post

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['titulo', 'subtitulo', 'texto', 'categoria', 'imagen']
    template_name = 'post_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='Colaborador').exists() or self.request.user.is_superuser

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['titulo', 'subtitulo', 'texto', 'categoria', 'imagen', 'activo']
    template_name = 'post_form.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        post = self.get_object()
        return (self.request.user == post.autor and self.request.user.groups.filter(name='Colaborador').exists()) or self.request.user.is_superuser

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        post = self.get_object()
        return (self.request.user == post.autor and self.request.user.groups.filter(name='Colaborador').exists()) or self.request.user.is_superuser

# Vistas para Comentario

class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    fields = ['texto']
    template_name = 'comentario_form.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post_detalle', kwargs={'id': self.kwargs['pk']})

class ComentarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comentario
    fields = ['texto']
    template_name = 'comentario_form.html'

    def test_func(self):
        comentario = self.get_object()
        return self.request.user == comentario.autor

    def get_success_url(self):
        return reverse_lazy('post_detalle', kwargs={'id': self.object.post.id})

class ComentarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comentario
    template_name = 'comentario_confirm_delete.html'

    def test_func(self):
        comentario = self.get_object()
        # Puede borrar el autor del comentario O el autor del post (Colaborador)
        es_autor_comentario = self.request.user == comentario.autor
        es_autor_post = self.request.user == comentario.post.autor
        return es_autor_comentario or es_autor_post

    def get_success_url(self):
        return reverse_lazy('post_detalle', kwargs={'id': self.object.post.id})
