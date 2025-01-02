from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm
from apps.products.models import Product  # Updated Import

# Register View
class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# Login View
class LoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

# Logout View
class LogoutView(BaseLogoutView):
    pass  # Use the default behavior

# Dashboard View
@login_required
def dashboard(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'users/dashboard.html', {'products': products})

    # user_name = request.user.username
    # return HttpResponse(f"Hello {user_name}, Welcome to your dashboard!")