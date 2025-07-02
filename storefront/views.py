from rest_framework import viewsets, permissions
from .models import Product # Add Order, ShippingRate later
from .serializers import ProductSerializer # Add OrderSerializer, etc. later

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to create, view, edit, and delete their products.
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the products
        for the currently authenticated user.
        """
        return Product.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Associate the product with the currently authenticated user on creation.
        """
        serializer.save(owner=self.request.user)
