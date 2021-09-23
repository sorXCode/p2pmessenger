#!/bin/bash
docker compose down web
docker compose up web & docker exec p2pmessenger_web python3 manage.py makemigrations