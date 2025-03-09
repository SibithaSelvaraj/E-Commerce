from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps import cart
from apps.payments.models import Payment
from .models import Cart, CartItem, Product
from django.views.decorators.http import require_POST
from decimal import Decimal
from apps.orders.models import Order, OrderItem
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()  # Fetch all items related to the cart
    # Fetch or create an order linked to the cart
    order = Order.objects.filter(cart=cart, status='Pending').first()
    if not order:
        order = Order.objects.create(cart=cart, status='Pending', user=request.user)
    # Ensure each cart item is added as an order item
    for cart_item in cart_items:
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=cart_item.product,
            defaults={
                'quantity': cart_item.quantity,
                'total_amount': cart_item.product.price * cart_item.quantity,
            }
        )
        if not created:
            # Update quantity and total_amount if the order item already exists
            order_item.quantity = cart_item.quantity
            order_item.total_amount = cart_item.product.price * cart_item.quantity
            order_item.save()
    # Prepare cart items for display
    processed_cart_items = []
    for item in cart_items:
        product = item.product
        unit_price = product.price
        quantity = item.quantity
        total_price = unit_price * quantity
        stock_availability = "In Stock" if product.stock > 0 else "Out of Stock"
        processed_cart_items.append({
            'product': product,
            'unit_price': unit_price,
            'quantity': quantity,
            'total_price': total_price,
            'stock_availability': stock_availability,
        })
    # Calculate subtotal, taxes, shipping, and grand total
    subtotal = sum(Decimal(item['total_price']) for item in processed_cart_items)
    taxes = subtotal * Decimal(0.0)  # Adjust tax rate as necessary
    shipping = Decimal(50)  # Flat shipping rate
    total_amount = subtotal + taxes + shipping
    # Update the order with these values
    order.subtotal = subtotal
    order.taxes = taxes
    order.shipping = shipping
    order.total_amount = total_amount
    order.save()
    print(Payment.objects.all())
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'cart_items': processed_cart_items,
        'subtotal': subtotal,
        'taxes': taxes,
        'shipping': shipping,
        'total_amount': total_amount,
        'order': order,
    })

def update_quantity(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if quantity > 0 and quantity <= product.stock:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            # Handle invalid quantity (e.g., out of stock or invalid input)
            pass
    return redirect('cart')

def checkout_view(request, order_id):
    # Fetch the order associated with the given order_id
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        # Update the order with the new shipping details from the form
        order.address = request.POST['address']
        order.state = request.POST['state']
        order.country = request.POST['country']
        order.postal_code = request.POST['postal_code']
        order.phone_number = request.POST['phone_number']
        order.landmark = request.POST.get('landmark', '')  # Optional
        order.save()
        # After updating shipping details, redirect to the payment page
        return redirect('process_payment', order_id=order.id)
    # Get all order items for the order
    order_items = OrderItem.objects.filter(order=order)
    # Prevent duplicates in the order summary
    order_summary = []
    for item in order_items:
        existing_item = next((entry for entry in order_summary if entry['id'] == item.product.id), None)
        if existing_item:
            existing_item['quantity'] += item.quantity
            existing_item['total_price'] += item.product.price * item.quantity
        else:
            order_summary.append({
                'id': item.product.id,
                'name': item.product.name,
                'quantity': item.quantity,
                'total_price': item.product.price * item.quantity,
            })
    # Calculate totals
    subtotal = sum(item['total_price'] for item in order_summary)
    taxes = subtotal * Decimal(0.0)  # Adjust tax calculation if necessary
    shipping = Decimal(50)  # Flat shipping rate
    total_amount = subtotal + taxes + shipping
    # Update order totals in the database
    order.subtotal = subtotal
    order.taxes = taxes
    order.shipping = shipping
    order.total_amount = total_amount
    order.save()
    print("checkout_view")
    print(order_summary)
    # Debugging logs (optional, remove in production)
    for item in order_summary:
        print(f"Product: {item['name']}, Quantity: {item['quantity']}, Total Price: {item['total_price']}")
    # Pass the cleaned order summary to the template
    context = {
        'order': order,
        'order_items': order_summary,  # Pass the cleaned summary instead of raw items
        'subtotal': subtotal,
        'taxes': taxes,
        'shipping': shipping,
        'total_amount': total_amount,
    }
    return render(request, 'cart/checkout.html', context)

def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        payment_data = {
            'order': order,
            'payment_method': request.POST['payment_method'],
            'payment_status': 'Completed',
            'transaction_id': 'TX123456',  # Replace with actual transaction ID from your payment gateway
        }
        payment = Payment.objects.create(**payment_data)
        # Update order status after payment
        order.status = 'Processing'
        order.save()
        print(Payment.objects.all())
        return redirect('payment_success')  # Redirect to payment success page
    # Pass the total amount to the payment form (useful for debugging or Razorpay integration)
    return render(request, 'payment_form.html', {'order': order, 'total_amount': order.total_amount})

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id)
    cart_item.delete()  # Remove item from cart
    return redirect('cart')