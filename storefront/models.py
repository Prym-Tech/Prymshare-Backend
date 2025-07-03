# storefront/models.py

from django.db import models
from users.models import CustomUser
from pages.models import Page

class Product(models.Model):
    """
    A physical product for sale in a user's storefront.
    """
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    image = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def owner(self):
        return self.page.owner

class ShippingRate(models.Model):
    """
    Merchant-defined shipping rates per location.
    """
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shipping_rates')
    location_name = models.CharField(max_length=200, help_text="e.g., 'Lagos Island', 'Abuja FCT'")
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.location_name} - N{self.rate}"

class Order(models.Model):
    """
    An order placed by a customer.
    """
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cod', 'Cash on Delivery'), # Cash on Delivery
    ]
    
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    customer_email = models.EmailField()
    customer_address = models.TextField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    paystack_ref = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    """
    An item within an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at time of purchase