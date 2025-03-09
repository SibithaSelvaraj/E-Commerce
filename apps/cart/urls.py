from django.urls import path
from .views import cart_view, add_to_cart, remove_from_cart, checkout_view, update_quantity
from . import views

urlpatterns = [
    path('', cart_view, name='cart'),
    path('add/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove-from-cart'),
    path('update_quantity/<int:product_id>/', update_quantity, name='update-quantity'),
    path('checkout/<int:order_id>/', views.checkout_view, name='checkout'),
    path('process_payment/<int:order_id>/', views.process_payment, name='process_payment'),
]
