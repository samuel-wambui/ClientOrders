from django.shortcuts import render

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Optionally, you could build a context dynamically.
    # Here we simply hard-code the API endpoints.
    context = {
        'api_endpoints': {
            'Customers': '/api/customers/',
            'Orders': '/api/orders/',
        }
    }
    return render(request, 'dashboard.html', context)

# core/views.py (add this function)
from django.shortcuts import redirect

def homepage(request):
    # If the user is authenticated, send them to the dashboard;
    # otherwise, show the home page with a login link.
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'homepage.html')
