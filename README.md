# Proyecto Final - Grupo 1

## Integrantes
- Esteban Nuñez
- Lorena Elisabeth Sotelo
- Juan Fabricio Milanesio
- Ricardo David Godoy

## Instrucciones de instalación para el equipo

1. Clonar el repositorio.
2. Crear un entorno virtual:
   `python -m venv .venv`
3. Activar el entorno:
   - Windows: `.\.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
4. Instalar dependencias:
   `pip install -r requirements.txt`
5. Realizar migraciones (necesario porque la DB no se sube):
   `python manage.py migrate`
6. Crear un superusuario propio:
   `python manage.py createsuperuser`
7. Correr el servidor:
   `python manage.py runserver`
