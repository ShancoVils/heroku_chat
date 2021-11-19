#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


import os
import django
from channels.routing import get_default_application
import channels

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_chat.settings')

django.setup()
application = get_default_application()