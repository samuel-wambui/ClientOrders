# oidc_custom_views.py
import logging
from mozilla_django_oidc.views import OIDCAuthenticationCallbackView

logger = logging.getLogger(__name__)

class CustomOIDCAuthenticationCallbackView(OIDCAuthenticationCallbackView):
    def get(self, request, *args, **kwargs):
        """
        Override the GET method to log the JWT token after the OIDC callback processing.
        """
        response = super().get(request, *args, **kwargs)
        # The OIDC response is stored in self.oidc_response.
        # The JWT (id_token) is typically part of this response.
        jwt_token = self.oidc_response.get("id_token")
        logger.info("JWT Token: %s", jwt_token)
        print("JWT Token:", jwt_token)
        return response
