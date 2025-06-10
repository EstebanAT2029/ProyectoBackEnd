# 🧾 ProyectoBackEnd - Sistema de Facturación para Hostales

Este proyecto es el backend de un sistema de facturación diseñado para hostales. Gestiona clientes, reservas, servicios, empleados y emisión de comprobantes electrónicos de forma segura y eficiente.

## 🚀 Tecnologías Utilizadas

- Python 3
- Django / Django REST Framework
- PostgreSQL
- JWT (Autenticación)
- Swagger / Redoc (Documentación de API)
- Cloudinary (Gestión de archivos multimedia)
- Docker (opcional para despliegue)

## 📁 Estructura del Proyecto


## 🔒 Funcionalidades

- CRUD completo de clientes, empleados, servicios y reservas.
- Generación y consulta de comprobantes electrónicos.
- Protección de rutas mediante autenticación JWT.
- Documentación interactiva con Swagger.
- Gestión de imágenes y documentos en la nube.

## 📦 Instalación y Ejecución

1. Clona el repositorio:
   ```bash
   git clone https://github.com/EstebanAT2029/ProyectoBackEnd.git
   cd ProyectoBackEnd


Ejecuta las migraciones y lanza el servidor:

bash
Copiar
Editar
python manage.py migrate
python manage.py runserver


🧪 Endpoints de la API
Puedes acceder a la documentación desde:

http://localhost:8000/api/docs/ (Swagger)

http://localhost:8000/api/redoc/ (Redoc)