from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from jwt import PyJWTError
from .models import User, Role
from .utils import decode_jwt_and_get_email
import logging
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)

logger.info("Django server started!")
# Upgrade user to admin
def upgrade_user_to_admin(request, email):
    user = get_object_or_404(User, email=email)  # Get user by email
    
    # Ensure the "admin" role exists
    admin_role, created = Role.objects.get_or_create(name="admin")  

    if admin_role in user.roles.all():
        return JsonResponse({"message": f"User {email} is already an admin."}, status=200)

    # Assign "admin" role
    user.roles.add(admin_role)

    # Set the user as staff so they can access the admin interface
    user.is_staff = True
    user.save()

    return JsonResponse({"message": f"User {email} upgraded to admin."}, status=200)


# Handle JWT login
User = get_user_model()

def jwt_login_view(request):
    logger.info("JWT Login view accessed.")

    try:
        email = decode_jwt_and_get_email(request)
        logger.debug(f"Decoded email from JWT: {email}")

        user, created = User.objects.get_or_create(email=email)

        if created:
            logger.info(f"New user created: {email}")
        else:
            logger.info(f"User already exists: {email}")

        return JsonResponse({"message": f"User {email} authenticated and registered."}, status=200)

    except PyJWTError as e:
        logger.error(f"JWT error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=401)
    
    except Exception as e:
        logger.error(f"Unexpected error during authentication: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)


