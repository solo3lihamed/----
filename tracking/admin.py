from django.contrib import admin
from django.utils.html import format_html
from .models import ShipmentStatus


@admin.register(ShipmentStatus)
class ShipmentStatusAdmin(admin.ModelAdmin):
    list_display = ['order', 'status_badge', 'status_ar', 'status_en', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order__order_number', 'order__tracking_code', 'notes']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('معلومات الحالة', {
            'fields': ('order', 'status', 'status_ar', 'status_en', 'notes')
        }),
        ('التاريخ', {
            'fields': ('created_at',)
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
        }
        color = status_colors.get(obj.status, '#808080')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">{}</span>',
            color,
            obj.status_ar
        )
    status_badge.short_description = 'الحالة'
