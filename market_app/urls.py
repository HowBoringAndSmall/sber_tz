from rest_framework import routers
from market_app.views import ProductViewSet, PurchaseViewSet, ProductSearchView

router = routers.SimpleRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'purchase', PurchaseViewSet, basename='purchase')
router.register(r'product/search', ProductSearchView, basename='product_search')
urlpatterns = router.urls
