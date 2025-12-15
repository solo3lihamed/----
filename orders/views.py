from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from perfumes.models import Perfume
from .models import Order, OrderItem
from tracking.models import ShipmentStatus
from .forms import OrderCreateForm


def order_create(request):
    """إنشاء طلب جديد"""
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, _('السلة فارغة'))
        return redirect('perfumes:list')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_amount = cart.get_total_price()
            order.save()
            
            # إنشاء عناصر الطلب
            for item in cart:
                perfume = item['perfume']
                perfume_image_url = ''
                if perfume.image and hasattr(perfume.image, 'url'):
                    try:
                        perfume_image_url = perfume.image.url
                    except ValueError:
                        # If there's no file associated with the image, leave it empty
                        perfume_image_url = ''

                OrderItem.objects.create(
                    order=order,
                    perfume_name_ar=perfume.name_ar,
                    perfume_name_en=perfume.name_en,
                    perfume_image=perfume_image_url,
                    quantity=item['quantity'],
                    price=item['price'],
                    size=perfume.size
                )
            
            # إنشاء أول حالة للتتبع
            ShipmentStatus.objects.create(
                order=order,
                status='pending'
            )
            
            # مسح السلة
            cart.clear()
            
            messages.success(request, _('تم إنشاء الطلب بنجاح'))
            return redirect('orders:success', order_id=order.id)
    else:
        # تعبئة البيانات تلقائياً للمستخدم المسجل
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'customer_name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
            }
        form = OrderCreateForm(initial=initial_data)
    
    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'orders/create.html', context)


def order_success(request, order_id):
    """صفحة نجاح الطلب"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'orders/success.html', context)


@login_required
def my_orders(request):
    """طلبات المستخدم"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'orders/my_orders.html', context)


def order_detail(request, order_number):
    """تفاصيل الطلب"""
    order = get_object_or_404(Order, order_number=order_number)
    context = {
        'order': order,
    }
    return render(request, 'orders/detail.html', context)
