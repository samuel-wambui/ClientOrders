# utils.py
from .models import User, Role
import jwt
from django.http import JsonResponse
from django.conf import settings

import logging
logger = logging.getLogger(__name__)
def decode_jwt_and_get_email(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning("Missing or invalid Authorization header")
        raise jwt.PyJWTError("Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]  # Extract token

    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = decoded.get("email")

        if not email:
            logger.error("JWT does not contain an email")
            raise jwt.PyJWTError("Invalid JWT payload: missing email")

        return email

    except jwt.ExpiredSignatureError:
        logger.error("JWT Error: Token has expired")
        raise jwt.PyJWTError("Token has expired")

    except jwt.DecodeError:
        logger.error("JWT Error: Invalid token")
        raise jwt.PyJWTError("Invalid token")

    except Exception as e:
        logger.exception(f"Unexpected JWT error: {str(e)}")
        raise jwt.PyJWTError("JWT processing error")

class JWTUserHandler:
    @staticmethod
    def handle_jwt_user(email):
        # Check if user exists, otherwise create them
        user, created = User.objects.get_or_create(email=email)
        if created:
            # Assign "user" role by default
            user.roles.add(Role.objects.get(name="user"))
        return user
