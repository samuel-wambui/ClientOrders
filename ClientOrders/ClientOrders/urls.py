from django.contrib import admin
from django.urls import path, include
from mozilla_django_oidc.views import OIDCAuthenticationRequestView, OIDCLogoutView
from core.views import homepage, dashboard

urlpatterns = [
    # Homepage
    path('', homepage, name='homepage'),
    
    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
    
    # Admin interface.
    path('admin/', admin.site.urls),
    
    # API endpoints.
    path('api/orders/', include('orders.urls')),
    path('api/authorization/', include('Authorization.urls')),
    
    # OIDC endpoints.
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('oidc/authenticate/', OIDCAuthenticationRequestView.as_view(), name='oidc_authenticate'),
    path('oidc/logout/', OIDCLogoutView.as_view(), name='oidc_logout'),

    # New URL pattern for "logout" that will resolve when you call {% url 'logout' %}
    path('logout/', OIDCLogoutView.as_view(), name='logout'),
]

