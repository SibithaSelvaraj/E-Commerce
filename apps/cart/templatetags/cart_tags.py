from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except TypeError:
        return 0  # Return 0 if values are not compatible for multiplication

@register.filter
def get_item(cart, product_id):
    return cart.items.filter(product_id=product_id).first() if cart else None