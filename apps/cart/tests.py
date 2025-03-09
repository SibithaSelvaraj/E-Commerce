# #from django.test import TestCase

# how to add product to cart

# this is my existing file structure
# vkcollections/
# ├── apps/
# │   ├── analytics/
# │   ├── cart/
# │   │   ├── migrations/
# │   │   ├── templates/
# │   │   │   ├── cart/
# │   │   │   │    ├── cart.html
# │   │   │   │    ├── checkout.html
# │   │   ├── templatetags/
# │   │   │   ├── cart_tags.py
# │   │   ├── admin.py
# │   │   ├── apps.py
# │   │   ├── forms.py
# │   │   ├── models.py
# │   |   ├── urls.py
# │   │   ├── views.py
# │   ├── orders/
# │   │   ├── migrations/
# │   │   ├── templates/
# │   │   │   ├── my_order_list.html
# │   │   ├── admin.py
# │   │   ├── apps.py
# │   │   ├── models.py
# │   |   ├── tests.py
# │   │   ├── views.py
# │   ├── payments/
# │   │   ├── migrations/
# │   │   ├── templates/
# │   │   │   ├── payment_form.html
# │   │   ├── admin.py
# │   │   ├── apps.py
# │   │   ├── models.py
# │   |   ├── urls.py
# │   │   ├── views.py
# │   ├── products/
# │   │   ├── migrations/
# │   │   ├── templates/
# │   │   │   ├── products/
# │   │   │   │    ├── product_list.html
# │   │   │   │    ├── create_product.html
# │   │   │   │    ├── update_product.html
# │   │   │   │    ├──delete_product.html
# │   │   ├── admin.py
# │   │   ├── apps.py
# │   │   ├── forms.py
# │   │   ├── models.py
# │   |   ├── urls.py
# │   │   ├── views.py
# │   ├── reviews/
# │   ├── users/
# |   |   ├── migrations/
# │   │   ├── templates/
# │   │   │   ├── registration/
# │   │   │   │    ├── password_reset_form.html
# │   │   │   │    ├── password_reset_done.html
# │   │   │   │    ├── password_reset_complete.html
# │   │   │   │    ├──password_reset_confirm.html
# │   │   │   ├── users/
# │   │   │   │    ├── dashboard.html
# │   │   │   │    ├── login.html
# │   │   │   │    ├── register.html
# │   │   ├── admin.py
# │   │   ├── apps.py
# │   │   ├── forms.py
# │   │   ├── models.py
# │   |   ├── urls.py
# │   │   ├── views.py
# ├── media/
# ├── product_images/
# ├── vkcollections/
# │   ├── _init_.py
# │   ├── asgi.py
# │   ├── settings.py
# │   ├── urls.py
# │   ├── wsgi.py
# ├── db.sqlite3
# ├── manage.py
# ├── requirements.txt

# cart/cart.html
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Your Cart</title>
#     <script src="https://cdn.tailwindcss.com"></script>
# </head>
# <body class="bg-gray-100 font-sans">
#     <div class="container mx-auto mt-10 p-5">
#         <h1 class="text-2xl font-bold mb-4 text-gray-800">Your Cart</h1>

#         {% load cart_tags %} <!-- Load custom template tags -->

#         {% if cart.items.count %}
#             <table class="table-auto w-full bg-white rounded-lg shadow-lg overflow-hidden">
#                 <thead class="bg-gray-800 text-white">
#                     <tr>
#                         <th class="px-4 py-2">Product</th>
#                         <th class="px-4 py-2">Quantity</th>
#                         <th class="px-4 py-2">Price</th>
#                         <th class="px-4 py-2">Total</th>
#                         <th class="px-4 py-2">Actions</th>
#                     </tr>
#                 </thead>
#                 <tbody>
#                     {% for item in cart.items.all %}
#                         <tr class="hover:bg-gray-100">
#                             <td class="px-4 py-2">{{ item.product.name }}</td>
#                             <td class="px-4 py-2">{{ item.quantity }}</td>
#                             <td class="px-4 py-2">${{ item.product.price }}</td>
#                             <td class="px-4 py-2">${{ item.quantity|multiply:item.product.price }}</td> <!-- Updated total calculation -->
#                             <td class="px-4 py-2">
#                                 <a href="{% url 'cart-remove' item.id %}" class="text-red-500 hover:underline">Remove</a> <!-- Example action -->
#                             </td>
#                         </tr>
#                     {% endfor %}
#                 </tbody>
#             </table>
#         {% else %}
#             <p class="text-gray-600">Your cart is empty.</p>
#         {% endif %}
#     </div>
# </body>
# </html>

# dashboard.html
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Dashboard</title>
#     <script src="https://cdn.tailwindcss.com"></script>
# </head>
# <body class="bg-gray-100">
#     <!-- First Division -->
#     <header class="flex justify-between items-center bg-gray-800 text-white p-4">
#         <div class="text-2xl font-bold">VK Collections</div>
#         <div class="flex items-center space-x-4">
#             <a href="{% url 'cart' %}" class="relative">
#                 <svg class="w-6 h-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
#                     <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-1.2 5.8A2 2 0 008 21h8a2 2 0 001.8-2.2L17 13M5.4 5H21M16 16v2M8 16v2" />
#                 </svg>
#                 <span class="absolute top-0 right-0 bg-red-500 text-white text-xs font-bold rounded-full px-1">
#                     {{ cart.items.count }}
#                 </span>
#             </a>
#             <form method="POST" action="{% url 'logout' %}">
#                 {% csrf_token %}
#                 <button type="submit" class="bg-white text-gray-500 px-4 py-2 rounded">Logout</button>
#             </form>
#         </div>
#     </header>
    

#     <!-- Navigation Bar -->
#     <nav class="bg-gray-200 p-4">
#         <ul class="flex space-x-4">
#             <li><a href="#" class="text-blue-500 hover:underline">Home</a></li>
#             <li><a href="#" class="text-blue-500 hover:underline">Electronics</a></li>
#             <li><a href="#" class="text-blue-500 hover:underline">Fashion</a></li>
#             <li><a href="#" class="text-blue-500 hover:underline">Books</a></li>
#             <li><a href="#" class="text-blue-500 hover:underline">Contact Us</a></li>
#         </ul>
#     </nav>

#     <!-- Second Division: Products -->
# <main class="p-4">
#     <h2 class="text-xl font-bold mb-4">Products</h2>
#     <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
#         {% for product in products %}
#             <div class="bg-white rounded-lg shadow-lg overflow-hidden">
#                 {% if product.image %}
#                     <img src="{{ product.image.url }}" alt="{{ product.name }}" class="w-full h-48 object-cover">
#                 {% else %}
#                     <div class="w-full h-48 bg-gray-200 flex items-center justify-center">
#                         <span class="text-gray-500">No Image</span>
#                     </div>
#                 {% endif %}
#                 <div class="p-4">
#                     <h3 class="text-lg font-bold text-gray-800">{{ product.name }}</h3>
#                     <p class="text-gray-600 mb-2">{{ product.description }}</p>
#                     <p class="text-gray-700 font-medium">Price: ${{ product.price }}</p>
#                     <p class="text-gray-700 font-medium">Stock: {{ product.stock }}</p>
#                     <p class="text-gray-700 font-medium">Category: {{ product.category.name }}</p>
#                 </div>
#             </div>
#         {% endfor %}
#     </div>
# </main>


#     <!-- Third Division: Contact and Google Map -->
#     <section class="grid grid-cols-2 gap-4 p-4">
#         <!-- Contact Form -->
#         <div class="bg-white shadow p-4 rounded">
#             <h2 class="text-xl font-bold mb-4">Contact Us</h2>
#             <form>
#                 <div class="mb-4">
#                     <label for="name" class="block text-sm font-medium">Name</label>
#                     <input type="text" id="name" name="name" class="w-full border border-gray-300 p-2 rounded">
#                 </div>
#                 <div class="mb-4">
#                     <label for="email" class="block text-sm font-medium">Email</label>
#                     <input type="email" id="email" name="email" class="w-full border border-gray-300 p-2 rounded">
#                 </div>
#                 <div class="mb-4">
#                     <label for="message" class="block text-sm font-medium">Message</label>
#                     <textarea id="message" name="message" rows="4" class="w-full border border-gray-300 p-2 rounded"></textarea>
#                 </div>
#                 <button type="submit" class="bg-gray-800 text-white text-center p-2 rounded">Submit</button>
#             </form>
#         </div>

#         <!-- Google Map -->
#         <div class="bg-white shadow p-4 rounded">
#             <h2 class="text-xl font-bold mb-4">Find Us</h2>
#             <iframe
#                 src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3151.8354345097376!2d144.95373541585695!3d-37.816279742021404!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6ad642af0f11fd81%3A0xf57765c88e8f5bdb!2sGoogle!5e0!3m2!1sen!2sus!4v1637066326472!5m2!1sen!2sus"
#                 width="100%" height="300" style="border:0;" allowfullscreen="" loading="lazy">
#             </iframe>
#         </div>
#     </section>

#     <!-- Fourth Division: Footer -->
#     <footer class="bg-gray-800 text-white text-center p-4">
#         <p>&copy; 2024 VK Collections. All Rights Reserved.</p>
#     </footer>
# </body>
# </html>
