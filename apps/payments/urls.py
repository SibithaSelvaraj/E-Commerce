from django.urls import path
from apps.payments.views import process_payment

urlpatterns = [
    # path('<int:order_id>/', views.payment_view, name='payment'),
    path('payment/<int:order_id>/', process_payment, name='process_payment'),
]
