import os
import django
from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission
from apps.posts.models import Post, Comentario

class PruebasDeRoles(TestCase):
    def setUp(self):
        # Crear grupos para las pruebas
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from apps.posts.models import Post, Comentario
        
        visitante, _ = Group.objects.get_or_create(name='Visitante')
        miembro, _ = Group.objects.get_or_create(name='Miembro')
        colaborador, _ = Group.objects.get_or_create(name='Colaborador')

        # Permisos para Colaborador
        ct_post = ContentType.objects.get_for_model(Post)
        ct_comentario = ContentType.objects.get_for_model(Comentario)
        
        permisos_colaborador = Permission.objects.filter(content_type__in=[ct_post, ct_comentario])
        colaborador.permissions.set(permisos_colaborador)

        # Permisos para Miembro
        permiso_add_comentario = Permission.objects.get(codename='add_comentario', content_type=ct_comentario)
        miembro.permissions.add(permiso_add_comentario)

        # Crear usuarios
        self.visitante = User.objects.create_user(username='visitante', password='password')
        self.miembro = User.objects.create_user(username='miembro', password='password')
        self.colaborador = User.objects.create_user(username='colaborador', password='password')
        
        # Asignar grupos (Miembro es asignado automáticamente por señal, pero aseguramos otros)
        colaborador_group = Group.objects.get(name='Colaborador')

        self.colaborador.groups.add(colaborador_group)
        
        # Visitante no tiene grupos extra (o tal vez solo Visitante si decidimos usarlo, pero usualmente ninguno)
        
    def test_asignacion_grupo_miembro(self):
        """Prueba que los nuevos usuarios obtienen el grupo Miembro automáticamente"""
        miembro_group = Group.objects.get(name='Miembro')
        self.assertTrue(self.miembro.groups.filter(name='Miembro').exists())
        self.assertTrue(self.visitante.groups.filter(name='Miembro').exists()) # Todos los nuevos usuarios lo obtienen por defecto

    def test_permisos_colaborador(self):
        """Prueba que Colaborador tiene permisos para agregar/cambiar/eliminar posts"""
        self.assertTrue(self.colaborador.has_perm('posts.add_post'))
        self.assertTrue(self.colaborador.has_perm('posts.change_post'))
        self.assertTrue(self.colaborador.has_perm('posts.delete_post'))
        
    def test_permisos_miembro(self):
        """Prueba que Miembro tiene permiso para agregar comentarios pero no posts"""
        self.assertTrue(self.miembro.has_perm('posts.add_comentario'))
        self.assertFalse(self.miembro.has_perm('posts.add_post'))

    def test_permisos_visitante(self):
        """Prueba Visitante (anónimo/nuevo usuario sin derechos extra)"""
        # Dado que asignamos automáticamente Miembro, un 'Visitante' que se registra ES un Miembro.
        # un verdadero visitante es anónimo.
        from django.contrib.auth.models import AnonymousUser
        anon = AnonymousUser()
        self.assertFalse(anon.has_perm('posts.add_comentario'))

