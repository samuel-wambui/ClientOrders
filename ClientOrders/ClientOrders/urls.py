from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Import Django's auth views
from mozilla_django_oidc.views import OIDCAuthenticationRequestView, OIDCLogoutView

# Import your custom views for homepage and dashboard.
from core.views import homepage, dashboard

urlpatterns = [
    # Homepage: Shows a login link if the user is not authenticated.
    path('', homepage, name='homepage'),
    
    # Dashboard: A protected view listing API endpoints.
    path('dashboard/', dashboard, name='dashboard'),
    
    # Admin interface.
    path('admin/', admin.site.urls),
    
    # API endpoints.
    path('api/orders/', include('orders.urls')),          # e.g., /api/orders/
    path('api/authorization/', include('Authorization.urls')),  # e.g., /api/authorization/
    
    # OIDC endpoints for authentication.
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('oidc/authenticate/', OIDCAuthenticationRequestView.as_view(), name='oidc_authenticate'),
    path('oidc/logout/', OIDCLogoutView.as_view(), name='oidc_logout'),

    # New URL pattern for "login" using Django's built-in LoginView.
    # This will render the template at templates/login.html.
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]
