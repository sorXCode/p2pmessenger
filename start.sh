#!/bin/bash     
python manage.py migrate
uvicorn --port 8080 --host 0.0.0.0 p2pmessenger.asgi:application --reload