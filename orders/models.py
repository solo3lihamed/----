from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
import uuid
import random
import string


class Order(models.Model):
    """الطلبات"""
    STATUS_CHOICES = [
        ('pending', _('قيد المراجعة')),
        ('confirmed', _('تم التأكيد')),
        ('preparing', _('قيد التحضير')),
        ('shipped', _('تم الشحن')),
        ('in_transit', _('في الطريق')),
        ('delivered', _('تم التسليم')),
        ('cancelled', _('ملغي')),
    ]

    order_number = models.CharField(_('رقم الطلب'), max_length=50, unique=True, blank=True)
    tracking_code = models.CharField(_('رمز التتبع'), max_length=20, unique=True, blank=True)
    
    # بيانات العميل
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('المستخدم'))
    customer_name = models.CharField(_('اسم العميل'), max_length=200)
    phone = models.CharField(_('رقم الهاتف'), max_length=20)
    email = models.EmailField(_('البريد الإلكتروني'), blank=True, null=True)
    address = models.TextField(_('العنوان'))
    city = models.CharField(_('المدينة'), max_length=100)
    notes = models.TextField(_('ملاحظات'), blank=True)
    
    # معلومات الطلب
    total_amount = models.DecimalField(_('المبلغ الإجمالي'), max_digits=10, decimal_places=2)
    status = models.CharField(_('الحالة'), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # التواريخ
    created_at = models.DateTimeField(_('تاريخ الإنشاء'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاريخ التحديث'), auto_now=True)

    class Meta:
        verbose_name = _('طلب')
        verbose_name_plural = _('الطلبات')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_number} - {self.customer_name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # توليد رقم طلب فريد
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        if not self.tracking_code:
            # توليد رمز تتبع فريد
            self.tracking_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)

    def get_status_display_ar(self):
        """عرض الحالة بالعربية"""
        status_map = {
            'pending': 'قيد المراجعة',
            'confirmed': 'تم التأكيد',
            'preparing': 'قيد التحضير',
            'shipped': 'تم الشحن',
            'in_transit': 'في الطريق',
            'delivered': 'تم التسليم',
            'cancelled': 'ملغي',
        }
        return status_map.get(self.status, self.status)

    def get_status_display_en(self):
        """عرض الحالة بالإنجليزية"""
        status_map = {
            'pending': 'Pending Review',
            'confirmed': 'Confirmed',
            'preparing': 'Preparing',
            'shipped': 'Shipped',
            'in_transit': 'In Transit',
            'delivered': 'Delivered',
            'cancelled': 'Cancelled',
        }
        return status_map.get(self.status, self.status)


class OrderItem(models.Model):
    """عناصر الطلب"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('الطلب'), related_name='items')
    perfume_name_ar = models.CharField(_('اسم المنتج بالعربية'), max_length=200)
    perfume_name_en = models.CharField(_('اسم المنتج بالإنجليزية'), max_length=200)
    perfume_image = models.CharField(_('صورة المنتج'), max_length=500, blank=True)
    quantity = models.PositiveIntegerField(_('الكمية'), default=1)
    price = models.DecimalField(_('السعر'), max_digits=10, decimal_places=2)
    size = models.CharField(_('الحجم'), max_length=50)

    class Meta:
        verbose_name = _('عنصر طلب')
        verbose_name_plural = _('عناصر الطلب')

    def __str__(self):
        return f"{self.perfume_name_ar} x {self.quantity}"

    def get_total(self):
        """حساب إجمالي العنصر"""
        return self.quantity * self.price
