#!/bin/bash

# Instalar dependencias
pip install -r requirements.txt

# Crear directorio de archivos estáticos si no existe
mkdir -p staticfiles

# Recopilar archivos estáticos
cd gestion
python manage.py collectstatic --noinput
