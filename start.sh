#!/bin/bash     
python manage.py migrate
daphne -b 0.0.0.0  -p 8080 p2pmessenger.asgi:application