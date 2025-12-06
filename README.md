# Proyecto Final - Grupo 1

## Integrantes
- Esteban Nuñez
- Lorena Elisabeth Sotelo
- Juan Fabricio Milanesio
- Ricardo David Godoy

## Instrucciones de instalación para el equipo

1. Clonar el repositorio. 
```bash
git clone https://github.com/fabricio00101/proyecto-final-grupo1.git
```

2. Ingresar a la carpeta proyecto-final-grupo1
```bash
cd proyecto-final-grupo1
```

3. Crear un entorno virtual:
   `python -m venv .venv`

4. Activar el entorno:
   - Windows: `.\.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`

5. Instalar dependencias:
   `pip install -r requirements.txt`

6. Crear un archivo llamado .env en la carpeta actual
```bash
DATABASE_URL=cadena-de-conexión-a-la-bd
```

7. Realizar migraciones (necesario porque la DB no se sube):
   `python manage.py migrate`

8. Crear un superusuario propio:
   `python manage.py createsuperuser`

9. Correr el servidor:
   `python manage.py runserver`

10. Ingresar en el navegador a http://127.0.0.1:8000   
