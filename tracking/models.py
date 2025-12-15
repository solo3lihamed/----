from django.db import models
from django.utils.translation import gettext_lazy as _
from orders.models import Order


class ShipmentStatus(models.Model):
    """تاريخ حالات الشحنة"""
    STATUS_CHOICES = [
        ('pending', _('طلب جديد')),
        ('confirmed', _('تم التأكيد')),
        ('preparing', _('قيد التحضير')),
        ('shipped', _('تم الشحن')),
        ('in_transit', _('في الطريق')),
        ('delivered', _('تم التسليم')),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('الطلب'), related_name='status_history')
    status = models.CharField(_('الحالة'), max_length=20, choices=STATUS_CHOICES)
    status_ar = models.CharField(_('الحالة بالعربية'), max_length=100)
    status_en = models.CharField(_('الحالة بالإنجليزية'), max_length=100)
    notes = models.TextField(_('ملاحظات'), blank=True)
    created_at = models.DateTimeField(_('تاريخ التحديث'), auto_now_add=True)

    class Meta:
        verbose_name = _('حالة الشحنة')
        verbose_name_plural = _('حالات الشحنة')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.order.order_number} - {self.status_ar}"

    def save(self, *args, **kwargs):
        # تعيين النصوص التلقائية إذا لم تكن موجودة
        if not self.status_ar:
            status_map_ar = {
                'pending': 'طلب جديد',
                'confirmed': 'تم التأكيد',
                'preparing': 'قيد التحضير',
                'shipped': 'تم الشحن',
                'in_transit': 'في الطريق',
                'delivered': 'تم التسليم',
            }
            self.status_ar = status_map_ar.get(self.status, self.status)
        
        if not self.status_en:
            status_map_en = {
                'pending': 'New Order',
                'confirmed': 'Confirmed',
                'preparing': 'Preparing',
                'shipped': 'Shipped',
                'in_transit': 'In Transit',
                'delivered': 'Delivered',
            }
            self.status_en = status_map_en.get(self.status, self.status)
        
        super().save(*args, **kwargs)
