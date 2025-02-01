"""
Production settings for ClientOrders.
"""

from .base import *
import os

DEBUG = False

# Set ALLOWED_HOSTS to include your production domains (Heroku apps, etc.)
ALLOWED_HOSTS = ['your-production-domain.com', '.herokuapp.com']

# In production, we assume that environment variables are already set (e.g., via Heroku config)
# Therefore, do not load a local .env file here.

OIDC_RP_CLIENT_ID = os.environ.get("OIDC_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = os.environ.get("OIDC_CLIENT_SECRET")

# Optionally, you can configure your production database here.
# For example, using dj_database_url to parse the DATABASE_URL environment variable:
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}")
    )
}

# You might also add production-specific settings such as security settings, logging adjustments, etc.
