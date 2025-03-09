from django.urls import path
from . import views

urlpatterns = [
    path('my-orders/', views.MyOrdersView.as_view(), name='my_orders'),
]
