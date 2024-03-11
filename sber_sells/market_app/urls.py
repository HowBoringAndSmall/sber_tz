from rest_framework import routers
from .views import ProductViewSet, PurchaseViewSet, ProductSearch

router = routers.SimpleRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'purchase', PurchaseViewSet, basename='purchase')
router.register(r'purchase/search', ProductSearch, basename='purchase_search')
urlpatterns = router.urls
