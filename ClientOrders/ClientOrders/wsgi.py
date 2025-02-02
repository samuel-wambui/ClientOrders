"""
WSGI config for ClientOrders project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

# Determine the project base directory (outer ClientOrders folder)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

# Now, the inner folder (ClientOrders) becomes accessible as a module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ClientOrders.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

