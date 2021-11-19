"""
ASGI config for online_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
from channels.routing import get_default_application
import channels

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_chat.settings')

django.setup()
ASGI_APPLICATION = "online_chat.asgi.application"
application = get_default_application()