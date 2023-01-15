from rest_framework.routers import DefaultRouter

from products.viewsets import ProductGeenericViewSet

router = DefaultRouter()
router.register('product-abc', ProductGeenericViewSet, basename='products')

urlpatterns = router.urls
