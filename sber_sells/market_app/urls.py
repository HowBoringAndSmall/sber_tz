from rest_framework import routers
from .views import ProductViewSet, PurchaseViewSet

router = routers.SimpleRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'purchase', PurchaseViewSet, basename='purchase')
urlpatterns = router.urls
