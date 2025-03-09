from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from apps.cart.models import Cart, CartItem
from apps.products.forms import ProductForm, ReviewForm 
from .models import Product, Review
from django.shortcuts import get_object_or_404, redirect

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

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all().order_by('-created_at')
        context['review_form'] = ReviewForm()

        # Check if the product is in the cart
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            context['product_in_cart'] = CartItem.objects.filter(cart=cart, product=self.object).exists()
        else:
            context['product_in_cart'] = False

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = self.object
            review.user = request.user
            review.save()
        return redirect('product-detail', pk=self.object.pk)        
    
    