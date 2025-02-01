from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, OrderViewSet

router = DefaultRouter()
router.register('customers', CustomerViewSet)  # Maps to /api/customers/
router.register('orders', OrderViewSet)       # Maps to /api/orders/

urlpatterns = router.urls  
