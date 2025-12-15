from .cart import Cart


def cart(request):
    """إضافة سلة التسوق لجميع القوالب"""
    return {'cart': Cart(request)}

