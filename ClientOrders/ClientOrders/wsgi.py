"""
WSGI config for ClientOrders project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

# Get the directory one level above ClientOrders/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add BASE_DIR to sys.path
sys.path.insert(0, BASE_DIR)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClientOrders.settings')

application = get_wsgi_application()
