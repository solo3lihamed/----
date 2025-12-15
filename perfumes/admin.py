from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Brand, Perfume


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_ar', 'name_en', 'slug', 'icon', 'created_at']
    search_fields = ['name_ar', 'name_en']
    prepopulated_fields = {'slug': ('name_en',)}
    list_filter = ['created_at']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']

    def logo_preview(self, obj):
        if obj.logo:
            try:
                return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.logo.url)
            except ValueError:
                # If there's no file associated with the logo, return a placeholder
                return format_html('<div style="width:50px; height:50px; background-color:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:5px;">-</div>')
        return '-'
    logo_preview.short_description = 'الشعار'


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name_ar', 'name_en', 'category', 'brand', 'price', 'discount_price', 'is_featured', 'in_stock', 'stock_quantity']
    list_filter = ['category', 'brand', 'is_featured', 'in_stock', 'created_at']
    search_fields = ['name_ar', 'name_en', 'description_ar', 'description_en']
    prepopulated_fields = {'slug': ('name_en',)}
    list_editable = ['is_featured', 'in_stock', 'price', 'discount_price']
    readonly_fields = ['created_at', 'updated_at', 'image_large_preview']
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('name_ar', 'name_en', 'slug', 'category', 'brand', 'size')
        }),
        ('الوصف', {
            'fields': ('description_ar', 'description_en')
        }),
        ('السعر', {
            'fields': ('price', 'discount_price')
        }),
        ('الصور', {
            'fields': ('image', 'image2', 'image3', 'image_large_preview')
        }),
        ('حالة المنتج', {
            'fields': ('is_featured', 'in_stock', 'stock_quantity')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            try:
                return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
            except ValueError:
                # If there's no file associated with the image, return a placeholder
                return format_html('<div style="width:50px; height:50px; background-color:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:5px;">-</div>')
        return '-'
    image_preview.short_description = 'صورة'

    def image_large_preview(self, obj):
        html = ''
        if obj.image:
            try:
                html += f'<img src="{obj.image.url}" width="200" style="border-radius: 10px; margin: 5px;" />'
            except ValueError:
                html += '<div style="width:200px; height:200px; background-color:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:10px; margin: 5px;">No Image</div>'
        if obj.image2:
            try:
                html += f'<img src="{obj.image2.url}" width="200" style="border-radius: 10px; margin: 5px;" />'
            except ValueError:
                html += '<div style="width:200px; height:200px; background-color:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:10px; margin: 5px;">No Image</div>'
        if obj.image3:
            try:
                html += f'<img src="{obj.image3.url}" width="200" style="border-radius: 10px; margin: 5px;" />'
            except ValueError:
                html += '<div style="width:200px; height:200px; background-color:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:10px; margin: 5px;">No Image</div>'
        if html:
            return format_html(html)
        return '-'
    image_large_preview.short_description = 'معاينة الصور'


# تخصيص واجهة الإدارة
admin.site.site_header = 'إدارة موقع عَبَق للعطور'
admin.site.site_title = 'عَبَق'
admin.site.index_title = 'لوحة التحكم'
