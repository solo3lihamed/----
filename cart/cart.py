from decimal import Decimal
from django.conf import settings
from perfumes.models import Perfume


class Cart:
    """إدارة سلة التسوق"""

    def __init__(self, request):
        """تهيئة سلة التسوق"""
        self.session = request.session
        cart = self.session.get(settings.SESSION_COOKIE_NAME.replace('sessionid', 'cart'))
        if not cart:
            # إنشاء سلة فارغة في الجلسة
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, perfume, quantity=1, override_quantity=False):
        """
        إضافة منتج إلى السلة أو تحديث كميته
        """
        perfume_id = str(perfume.id)
        if perfume_id not in self.cart:
            self.cart[perfume_id] = {
                'quantity': 0,
                'price': str(perfume.get_price())
            }
        if override_quantity:
            self.cart[perfume_id]['quantity'] = quantity
        else:
            self.cart[perfume_id]['quantity'] += quantity
        self.save()

    def save(self):
        """حفظ التغييرات في الجلسة"""
        self.session.modified = True

    def remove(self, perfume):
        """إزالة منتج من السلة"""
        perfume_id = str(perfume.id)
        if perfume_id in self.cart:
            del self.cart[perfume_id]
            self.save()

    def __iter__(self):
        """
        التكرار عبر عناصر السلة وإحضار المنتجات من قاعدة البيانات
        """
        perfume_ids = self.cart.keys()
        perfumes = Perfume.objects.filter(id__in=perfume_ids)
        cart = self.cart.copy()

        for perfume in perfumes:
            cart[str(perfume.id)]['perfume'] = perfume

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """حساب عدد العناصر في السلة"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """حساب السعر الإجمالي"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """مسح السلة"""
        del self.session['cart']
        self.save()

