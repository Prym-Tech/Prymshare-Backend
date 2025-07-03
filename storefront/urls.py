from django.urls import path, include
from rest_framework_nested import routers
from .views import ProductViewSet

# This creates a router that will handle the nested URLs for products.
# It will generate URLs like:
# /pages/1/products/
# /pages/1/products/123/
router = routers.SimpleRouter()
router.register(r'products', ProductViewSet, basename='page-products')

urlpatterns = [
    path('', include(router.urls)),
]