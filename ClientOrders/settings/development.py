"""
Development settings for ClientOrders.
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Load environment variables from your local .env file.
# (Ensure the path points to your local .env file.)
from dotenv import load_dotenv
env_file_path = r'C:\Users\wamalwa\OrdersApp\ClientOrders\ClientOrders\.env'
load_dotenv(dotenv_path=env_file_path)

# Now that the environment variables are loaded, override the OIDC settings if needed.
OIDC_RP_CLIENT_ID = os.environ.get("OIDC_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = os.environ.get("OIDC_CLIENT_SECRET")
print("OIDC_CLIENT_ID:", OIDC_RP_CLIENT_ID)
print("OIDC_CLIENT_SECRET:", OIDC_RP_CLIENT_SECRET)

# You can keep using the sqlite3 database in development.
