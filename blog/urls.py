"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import index
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),

    path('posts/', include('apps.posts.urls')),
    
    # Login
    path('auth/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    # Rutas de Auth de Django (Login, Logout, Password Reset)
    path('auth/', include('django.contrib.auth.urls')),
    # Rutas de la app usuarios (Registro)
    path('usuarios/', include('apps.usuarios.urls'))
]
    
