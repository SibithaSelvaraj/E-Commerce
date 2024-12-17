from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields = ['name', 'description', 'slug', 'price', 'stock', 'category', 'image', 'is_active']
