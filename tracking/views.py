from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from orders.models import Order
from .models import ShipmentStatus


def track_shipment(request):
    """تتبع الشحنة"""
    order = None
    status_history = None
    
    if request.method == 'POST':
        tracking_code = request.POST.get('tracking_code', '').strip()
        
        if tracking_code:
            try:
                order = Order.objects.get(tracking_code=tracking_code)
                status_history = ShipmentStatus.objects.filter(order=order).order_by('created_at')
            except Order.DoesNotExist:
                messages.error(request, _('رمز التتبع غير صحيح'))
        else:
            messages.error(request, _('الرجاء إدخال رمز التتبع'))
    
    # تحديد المراحل الست
    all_statuses = ['pending', 'confirmed', 'preparing', 'shipped', 'in_transit', 'delivered']
    status_labels_ar = {
        'pending': 'طلب جديد',
        'confirmed': 'تم التأكيد',
        'preparing': 'قيد التحضير',
        'shipped': 'تم الشحن',
        'in_transit': 'في الطريق',
        'delivered': 'تم التسليم',
    }
    status_labels_en = {
        'pending': 'New Order',
        'confirmed': 'Confirmed',
        'preparing': 'Preparing',
        'shipped': 'Shipped',
        'in_transit': 'In Transit',
        'delivered': 'Delivered',
    }
    status_icons = {
        'pending': 'fa-clock',
        'confirmed': 'fa-check-circle',
        'preparing': 'fa-box',
        'shipped': 'fa-shipping-fast',
        'in_transit': 'fa-truck',
        'delivered': 'fa-home',
    }
    
    # تحديد الحالة الحالية
    current_status_index = -1
    if order:
        try:
            current_status_index = all_statuses.index(order.status)
        except ValueError:
            current_status_index = -1
    
    context = {
        'order': order,
        'status_history': status_history,
        'all_statuses': all_statuses,
        'status_labels_ar': status_labels_ar,
        'status_labels_en': status_labels_en,
        'status_icons': status_icons,
        'current_status_index': current_status_index,
    }
    return render(request, 'tracking/track.html', context)
