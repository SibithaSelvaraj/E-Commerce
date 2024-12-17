from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.products.forms import ProductForm 
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 10  # Optional: Pagination (10 products per page)

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create_product.html'
    success_url = reverse_lazy('product-list') #reverse_lazy return back to product-list

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/update_product.html'
    success_url = reverse_lazy('product-list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/delete_product.html'
    success_url = reverse_lazy('product-list')

# This is model, write a list view (CBV) for this model as i am doing e commerce list view page. give me a basic template too and the url for it.
