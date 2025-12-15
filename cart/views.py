from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from perfumes.models import Perfume
from .cart import Cart


def cart_detail(request):
    """عرض سلة التسوق"""
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_add(request, perfume_id):
    """إضافة منتج إلى السلة"""
    cart = Cart(request)
    perfume = get_object_or_404(Perfume, id=perfume_id)
    
    if not perfume.in_stock:
        messages.error(request, _('عذراً، هذا المنتج غير متوفر حالياً'))
        return redirect(request.META.get('HTTP_REFERER', 'perfumes:list'))
    
    quantity = int(request.POST.get('quantity', 1))
    cart.add(perfume=perfume, quantity=quantity)
    messages.success(request, _('تم إضافة المنتج إلى السلة بنجاح'))
    
    return redirect(request.META.get('HTTP_REFERER', 'perfumes:list'))


@require_POST
def cart_remove(request, perfume_id):
    """إزالة منتج من السلة"""
    cart = Cart(request)
    perfume = get_object_or_404(Perfume, id=perfume_id)
    cart.remove(perfume)
    messages.success(request, _('تم إزالة المنتج من السلة'))
    
    return redirect('cart:detail')


@require_POST
def cart_update(request, perfume_id):
    """تحديث كمية منتج في السلة"""
    cart = Cart(request)
    perfume = get_object_or_404(Perfume, id=perfume_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart.add(perfume=perfume, quantity=quantity, override_quantity=True)
        messages.success(request, _('تم تحديث السلة'))
    else:
        cart.remove(perfume)
        messages.success(request, _('تم إزالة المنتج من السلة'))
    
    return redirect('cart:detail')


def cart_clear(request):
    """مسح السلة"""
    cart = Cart(request)
    cart.clear()
    messages.success(request, _('تم مسح السلة'))
    
    return redirect('cart:detail')
