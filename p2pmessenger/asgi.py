"""
ASGI config for p2pmessenger project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
import django
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p2pmessenger.settings')
django.setup()


asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
    'http': asgi_application,
})
