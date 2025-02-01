# urls.py
from django.urls import path
from . import views
from .oidc_custom_views import CustomOIDCAuthenticationCallbackView


urlpatterns = [
     path('oidc/callback/', CustomOIDCAuthenticationCallbackView.as_view(), name='oidc_callback'),
    path('upgrade_user_to_admin/<str:email>/', views.upgrade_user_to_admin, name='upgrade_user_to_admin'),  # Email in URL
]

