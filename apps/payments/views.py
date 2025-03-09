from django.shortcuts import render, redirect
from apps.orders.models import Order
from apps.payments.models import Payment
from django.conf import settings
import razorpay

def process_payment(request, order_id):
    print(1)
    order = Order.objects.get(id=order_id)
    print(f"Order Total Amount: {order.total_amount}")
    print(2)
    # if request.method == "POST":
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
        # Assuming payment details are posted
    print(3)
        # Create Razorpay order
    razorpay_order = client.order.create({
        "amount": int(order.total_amount * 100),  # Amount in paise
        "currency": "INR",
        "receipt": f"order_rcptid_{order.id}",
        "payment_capture": 1,  # Auto capture payment
    })
    # Save Razorpay order ID in the database
    order.razorpay_order_id = razorpay_order['id']
    order.save()
    print(4)
    context = {
        'order': order,
        'razorpay_key': settings.RAZORPAY_KEY,
        'amount': int(order.total_amount * 100),  # Amount in paise
        'razorpay_order_id': razorpay_order['id'],    }
    print(context)
    print(5)
    return render(request, 'payment_form.html', context)
    print(6)
print(7)
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Payment
# from apps.orders.models import Order

# @login_required
# def payment_view(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     if request.method == 'POST':
#         payment_method = request.POST.get('payment_method')
#         payment = Payment.objects.create(
#             user=request.user,
#             order=order,
#             payment_method=payment_method,
#             total_amount=order.total_amount
#         )
#         payment.payment_status = 'Completed'  # Simulating a successful payment
#         payment.save()
#         return redirect('payment-success', payment.id)

#     return render(request, 'cart/payment.html', {'order': order})
