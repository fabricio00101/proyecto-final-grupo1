from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Categoria, Comentario
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

# Create your views here.

# Esta función busca las publicaciones en la base de datos y las manda al HTML
def listar_publicaciones(request):
    # Busca todas las publicaciones
    publicaciones = Post.objects.all()

    # Sistema de filtrado por categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        publicaciones = publicaciones.filter(categoria_id=categoria_id)

    # Sistema de ordenamiento
    orden = request.GET.get('orden')
    if orden == 'antiguo':
        publicaciones = publicaciones.order_by('publicado') #Ascendente
    elif orden == 'alfabetico':
        publicaciones = publicaciones.order_by('titulo') # A-Z
    elif orden == 'alfabetico_inv':
        publicaciones = publicaciones.order_by('-titulo') # Z-A
    else:
        publicaciones = publicaciones.order_by('-publicado') #Por defecto: Recientes primero

    categorias = Categoria.objects.all()

    contexto = {
        'publicaciones': publicaciones,
        'categorias': categorias,
    }
    return render(request, 'lista_publicaciones.html', contexto)


def detalle_publicacion(request, id):
    publicacion = get_object_or_404(Post, id=id)
    comentarios = publicacion.comentarios.all()
    contexto={
        'publicacion': publicacion,
        'comentarios': comentarios
    }
    return render(request, 'detalle_publicacion.html', contexto)

# Vistas para Publicación

class PublicacionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['titulo', 'subtitulo', 'texto', 'categoria', 'imagen']
    template_name = 'publicacion_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='Colaborador').exists() or self.request.user.is_superuser

class PublicacionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['titulo', 'subtitulo', 'texto', 'categoria', 'imagen', 'activo']
    template_name = 'publicacion_form.html'
    success_url = reverse_lazy('index')
    pk_url_kwarg = 'id'

    def test_func(self):
        publicacion = self.get_object()
        return (self.request.user == publicacion.autor and self.request.user.groups.filter(name='Colaborador').exists()) or self.request.user.is_superuser

class PublicacionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'publicacion_confirm_delete.html'
    success_url = reverse_lazy('index')
    pk_url_kwarg = 'id'

    def test_func(self):
        publicacion = self.get_object()
        return (self.request.user == publicacion.autor and self.request.user.groups.filter(name='Colaborador').exists()) or self.request.user.is_superuser

# Vistas para Comentario

class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    fields = ['texto']
    template_name = 'comentario_form.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.post_id = self.kwargs['id']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('publicaciones:detalle', kwargs={'id': self.kwargs['id']})

class ComentarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comentario
    fields = ['texto']
    template_name = 'comentario_form.html'
    pk_url_kwarg = 'id'

    def test_func(self):
        comentario = self.get_object()
        # Puede editar si es el autor del comentario, o el autor de la publicación, o superuser
        return (
            self.request.user == comentario.autor
            or self.request.user == comentario.post.autor
            or self.request.user.is_superuser
        )

    def get_success_url(self):
        return reverse_lazy('publicaciones:detalle', kwargs={'id': self.object.post.id})

class ComentarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comentario
    template_name = 'comentario_confirm_delete.html'
    pk_url_kwarg = 'id'

    def test_func(self):
        comentario = self.get_object()
        # Puede eliminar si es el autor del comentario, el autor de la publicación, o superuser
        return (
            self.request.user == comentario.autor
            or self.request.user == comentario.post.autor
            or self.request.user.is_superuser
        )

    def get_success_url(self):
        return reverse_lazy('publicaciones:detalle', kwargs={'id': self.object.post.id})

