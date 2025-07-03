from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from .models import Product
from pages.models import Page
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the products for the
        page specified in the URL, owned by the current user.
        """
        # --- CHANGE START ---
        # This ensures we are fetching products for the specific page from the URL
        page_pk = self.kwargs.get('page_pk')
        if page_pk:
            # This is the key change: filter products by the page's primary key.
            return Product.objects.filter(page__pk=page_pk, page__owner=self.request.user).order_by('-created_at')
        # Return no products if no page is specified
        return Product.objects.none()
        # --- CHANGE END ---


    def perform_create(self, serializer):
        """
        Associate the product with the page from the URL.
        """
        # --- CHANGE START ---
        # This ensures that when a product is created, it's linked to the correct page.
        page_pk = self.kwargs.get('page_pk')
        page = get_object_or_404(Page, pk=page_pk, owner=self.request.user)
        serializer.save(page=page)