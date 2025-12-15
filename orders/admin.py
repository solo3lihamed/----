from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem
from tracking.models import ShipmentStatus


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['perfume_name_ar', 'perfume_name_en', 'quantity', 'price', 'size', 'get_total']
    can_delete = False

    def get_total(self, obj):
        return f"{obj.get_total()} ريال"
    get_total.short_description = 'الإجمالي'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'phone', 'city', 'total_amount', 'status_badge', 'created_at']
    list_filter = ['status', 'city', 'created_at']
    search_fields = ['order_number', 'tracking_code', 'customer_name', 'phone', 'email']
    readonly_fields = ['order_number', 'tracking_code', 'total_amount', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('معلومات الطلب', {
            'fields': ('order_number', 'tracking_code', 'status', 'total_amount')
        }),
        ('معلومات العميل', {
            'fields': ('user', 'customer_name', 'phone', 'email', 'address', 'city', 'notes')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def status_badge(self, obj):
        status_colors = {
            'pending': '#FFA500',
            'confirmed': '#4169E1',
            'preparing': '#9370DB',
            'shipped': '#20B2AA',
            'in_transit': '#FFD700',
            'delivered': '#32CD32',
            'cancelled': '#DC143C',
        }
        color = status_colors.get(obj.status, '#808080')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display_ar()
        )
    status_badge.short_description = 'الحالة'

    def save_model(self, request, obj, form, change):
        """حفظ الطلب وتحديث سجل التتبع"""
        if change:  # إذا كان تحديث
            old_obj = Order.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                # تغيرت الحالة، إنشاء سجل في التتبع
                ShipmentStatus.objects.create(
                    order=obj,
                    status=obj.status
                )
        else:  # طلب جديد
            super().save_model(request, obj, form, change)
            # إنشاء أول سجل في التتبع
            ShipmentStatus.objects.create(
                order=obj,
                status=obj.status
            )
            return
        
        super().save_model(request, obj, form, change)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'perfume_name_ar', 'quantity', 'price', 'get_total']
    list_filter = ['order__created_at']
    search_fields = ['perfume_name_ar', 'perfume_name_en', 'order__order_number']

    def get_total(self, obj):
        return f"{obj.get_total()} ريال"
    get_total.short_description = 'الإجمالي'
