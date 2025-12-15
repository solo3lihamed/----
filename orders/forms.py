from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """نموذج إنشاء الطلب"""
    
    class Meta:
        model = Order
        fields = ['customer_name', 'phone', 'email', 'address', 'city', 'notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': _('الاسم الكامل')
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': _('رقم الهاتف (05xxxxxxxx)')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': _('البريد الإلكتروني (اختياري)')
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': _('العنوان الكامل'),
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': _('المدينة')
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': _('ملاحظات إضافية (اختياري)'),
                'rows': 3
            }),
        }

