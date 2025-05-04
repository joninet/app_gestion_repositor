#!/bin/bash

# Asegurarnos de que estamos en el directorio correcto
echo "Current directory: $(pwd)"

# Verificar qué comandos están disponibles
echo "Python version:"
which python || which python3

echo "Pip version:"
which pip || which pip3

# Intentar diferentes comandos de Python
if command -v python3 &> /dev/null; then
    echo "Using python3..."
    PYTHON_CMD="python3"
    PIP_CMD="python3 -m pip"
elif command -v python &> /dev/null; then
    echo "Using python..."
    PYTHON_CMD="python"
    PIP_CMD="python -m pip"
else
    echo "Python not found!"
    exit 1
fi

# Instalar dependencias
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt

# Crear directorio de archivos estáticos si no existe
echo "Creating staticfiles directory..."
mkdir -p staticfiles

# Recopilar archivos estáticos
echo "Collecting static files..."
cd gestion
$PYTHON_CMD manage.py collectstatic --noinput
