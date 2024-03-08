from rest_framework import routers
from .views import ProductViewSet, PurchaseViewSet

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'purchases', PurchaseViewSet, basename='purchase')
router.register(r'purchases/client_purchase_with_product', PurchaseViewSet, basename='client_purchase_with_product')
urlpatterns = router.urls
