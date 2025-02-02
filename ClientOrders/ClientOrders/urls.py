"""
URL configuration for orders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mozilla_django_oidc.views import OIDCAuthenticationRequestView, OIDCLogoutView

# Import your custom views for homepage and dashboard.
# Make sure you have implemented these views in, for example, core/views.py.
from core.views import homepage, dashboard

urlpatterns = [
    # Homepage: Shows a login link if the user is not authenticated.
    path('', homepage, name='homepage'),
    
    # Dashboard: A protected view listing API endpoints (or other post-login info).
    path('dashboard/', dashboard, name='dashboard'),
    
    # Admin interface.
    path('admin/', admin.site.urls),
    
    # API endpoints: Adjust base paths as needed.
    path('api/orders/', include('orders.urls')),          # e.g., /api/orders/
    path('api/authorization/', include('Authorization.urls')),  # e.g., /api/authorization/
    
    # OIDC endpoints for authentication.
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('oidc/authenticate/', OIDCAuthenticationRequestView.as_view(), name='oidc_authenticate'),
    path('oidc/logout/', OIDCLogoutView.as_view(), name='oidc_logout'),
]
