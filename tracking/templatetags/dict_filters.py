from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary"""
    return dictionary.get(key, '')

@register.filter
def multiply(value, arg):
    """Multiply value by arg"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """Divide value by arg"""
    try:
        return int(value) / int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

