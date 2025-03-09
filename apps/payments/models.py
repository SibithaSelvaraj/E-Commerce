from django.db import models
class Payment(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='payments_payments')
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, default='Pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# from django.db import models
# from django.contrib.auth.models import User
# from apps.orders.models import Order
# from django.conf import settings

# class Payment(models.Model):
#     user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_orders', )
#     payment_method = models.CharField(max_length=50, choices=[('Credit Card', 'Credit Card'), ('PayPal', 'PayPal')])
#     payment_status = models.CharField(max_length=50, default='Pending')
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"{self.user.username} - {self.payment_method} - {self.payment_status}"
