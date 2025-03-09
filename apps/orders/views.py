from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .models import Order

# Create a view to display the orders
class MyOrdersView(TemplateView):
    template_name = 'orders/my_order_list.html'

def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect if not authenticated
        # Filter orders for the logged-in user
    orders = Order.objects.filter(user=request.user, status='completed')  # Assuming status indicates completion
    context = {
        'orders': orders,
    }
    return render(request, 'orders/my_order_list.html', context)
