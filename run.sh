#!/bin/bash

# Iniciar el servidor Flask (backend)
cd backend/
python app.py &

# Esperar un momento para que el servidor Flask se inicie
sleep 5

# Navegar al directorio de tu proyecto Django (cambia la ruta si es necesario)
cd ..
cd frontend/

# Iniciar el servidor Django (frontend)
python manage.py runserver
