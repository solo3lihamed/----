from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """فئات العطور"""
    name_ar = models.CharField(_('الاسم بالعربية'), max_length=100)
    name_en = models.CharField(_('الاسم بالإنجليزية'), max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(_('أيقونة'), max_length=50, help_text='Font Awesome icon class')
    description_ar = models.TextField(_('الوصف بالعربية'), blank=True)
    description_en = models.TextField(_('الوصف بالإنجليزية'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('فئة')
        verbose_name_plural = _('الفئات')
        ordering = ['name_ar']

    def __str__(self):
        return self.name_ar

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)


class Brand(models.Model):
    """العلامات التجارية"""
    name = models.CharField(_('الاسم'), max_length=100)
    logo = models.ImageField(_('الشعار'), upload_to='brands/', blank=True, null=True)
    description_ar = models.TextField(_('الوصف بالعربية'), blank=True)
    description_en = models.TextField(_('الوصف بالإنجليزية'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('علامة تجارية')
        verbose_name_plural = _('العلامات التجارية')
        ordering = ['name']

    def __str__(self):
        return self.name


class Perfume(models.Model):
    """المنتجات (العطور)"""
    name_ar = models.CharField(_('الاسم بالعربية'), max_length=200)
    name_en = models.CharField(_('الاسم بالإنجليزية'), max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description_ar = models.TextField(_('الوصف بالعربية'))
    description_en = models.TextField(_('الوصف بالإنجليزية'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('الفئة'), related_name='perfumes')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_('العلامة التجارية'), related_name='perfumes')
    price = models.DecimalField(_('السعر'), max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(_('سعر الخصم'), max_digits=10, decimal_places=2, blank=True, null=True)
    size = models.CharField(_('الحجم'), max_length=50, help_text='مثال: 100ml, 50ml')
    image = models.ImageField(_('الصورة الرئيسية'), upload_to='perfumes/')
    image2 = models.ImageField(_('صورة إضافية 1'), upload_to='perfumes/', blank=True, null=True)
    image3 = models.ImageField(_('صورة إضافية 2'), upload_to='perfumes/', blank=True, null=True)
    is_featured = models.BooleanField(_('منتج مميز'), default=False)
    in_stock = models.BooleanField(_('متوفر'), default=True)
    stock_quantity = models.PositiveIntegerField(_('الكمية'), default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('عطر')
        verbose_name_plural = _('العطور')
        ordering = ['-created_at']

    def __str__(self):
        return self.name_ar

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)

    def get_price(self):
        """يرجع السعر بعد الخصم إن وجد"""
        if self.discount_price:
            return self.discount_price
        return self.price

    def get_discount_percentage(self):
        """حساب نسبة الخصم"""
        if self.discount_price and self.price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0
