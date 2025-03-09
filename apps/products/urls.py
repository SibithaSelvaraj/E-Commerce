from django.urls import path, include
from .views import ProductDetailView, ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),

    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

]
