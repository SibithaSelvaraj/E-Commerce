from django.db import models
from django.shortcuts import render
from apps.cart.models import Cart
from apps.users.models import User
from apps.products.models import Product
from decimal import Decimal
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.CharField(max_length=100,default='x')
    state = models.CharField(max_length=100,default='Tamilnadu')
    country = models.CharField(max_length=100,default='India')
    postal_code = models.CharField(max_length=20,default=000000)
    phone_number = models.CharField(max_length=10,default=0)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    def calculate_total(self):
        # Calculate the subtotal, tax, shipping, and total amount
        subtotal = sum(item.total_amount for item in self.items.all())
        self.tax = subtotal * Decimal(0.0)  # Assuming a 0% tax rate, adjust as necessary
        self.shipping = Decimal(50)  # Fixed shipping cost, change as per requirement
        self.total_amount = subtotal + self.tax + self.shipping
        self.save()
    def update_status(self, status):
        self.status = status
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    def save(self, *args, **kwargs):
        self.total_amount = self.product.price * self.quantity  # Calculate total cost for this item
        super().save(*args, **kwargs)

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders_payments')
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=1.0)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def process_payment(self, transaction_id, payment_status):
        self.transaction_id = transaction_id
        self.payment_status = payment_status
        self.save()
        # Once payment is successful, update the order status
        if payment_status == 'success':
            self.order.update_status('Processing')
