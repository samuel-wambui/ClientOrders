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
from django.views.generic.base import RedirectView

from django.urls import path
from orders.views import api_dashboard  # Import the view

urlpatterns = [
     path('', RedirectView.as_view(pattern_name='oidc_authenticate', permanent=False), name='home'),
    path('dashboard/', api_dashboard, name='dashboard'),
    path('api/orders/', include('orders.urls')),
    path('api/authorization/', include('Authorization.urls')),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('oidc/authenticate/', OIDCAuthenticationRequestView.as_view(), name='oidc_authenticate'),
    path('oidc/logout/', OIDCLogoutView.as_view(), name='oidc_logout'),
]
