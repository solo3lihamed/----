"""
سكريبت لإضافة بيانات تجريبية للموقع
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from perfumes.models import Category, Brand, Perfume
from django.contrib.auth.models import User

# إنشاء superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@abaq.com', 'admin123')
    print('✓ تم إنشاء superuser: admin / admin123')

# إنشاء الفئات
categories_data = [
    {'name_ar': 'عطور رجالية', 'name_en': 'Men\'s Perfumes', 'icon': 'fas fa-male', 'description_ar': 'عطور فاخرة للرجال', 'description_en': 'Luxury perfumes for men'},
    {'name_ar': 'عطور نسائية', 'name_en': 'Women\'s Perfumes', 'icon': 'fas fa-female', 'description_ar': 'عطور راقية للنساء', 'description_en': 'Elegant perfumes for women'},
    {'name_ar': 'عطور عود', 'name_en': 'Oud Perfumes', 'icon': 'fas fa-fire', 'description_ar': 'عطور عود فاخرة', 'description_en': 'Luxury oud perfumes'},
    {'name_ar': 'عطور فرنسية', 'name_en': 'French Perfumes', 'icon': 'fas fa-heart', 'description_ar': 'عطور فرنسية أصلية', 'description_en': 'Original French perfumes'},
    {'name_ar': 'عطور منعشة', 'name_en': 'Fresh Perfumes', 'icon': 'fas fa-wind', 'description_ar': 'عطور منعشة للصيف', 'description_en': 'Refreshing perfumes for summer'},
    {'name_ar': 'عطور شرقية', 'name_en': 'Oriental Perfumes', 'icon': 'fas fa-star', 'description_ar': 'عطور شرقية أصيلة', 'description_en': 'Authentic oriental perfumes'},
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name_en=cat_data['name_en'],
        defaults=cat_data
    )
    if created:
        print(f'✓ تم إنشاء الفئة: {cat_data["name_ar"]}')

# إنشاء العلامات التجارية
brands_data = [
    {'name': 'Dior', 'description_ar': 'علامة فرنسية فاخرة', 'description_en': 'Luxury French brand'},
    {'name': 'Chanel', 'description_ar': 'عطور راقية من شانيل', 'description_en': 'Elegant perfumes from Chanel'},
    {'name': 'Versace', 'description_ar': 'علامة إيطالية مميزة', 'description_en': 'Distinctive Italian brand'},
    {'name': 'Tom Ford', 'description_ar': 'عطور فاخرة من توم فورد', 'description_en': 'Luxury perfumes from Tom Ford'},
    {'name': 'Armani', 'description_ar': 'أرماني الإيطالية', 'description_en': 'Italian Armani'},
    {'name': 'Rasasi', 'description_ar': 'علامة عربية مشهورة', 'description_en': 'Famous Arab brand'},
]

for brand_data in brands_data:
    brand, created = Brand.objects.get_or_create(
        name=brand_data['name'],
        defaults=brand_data
    )
    if created:
        print(f'✓ تم إنشاء العلامة التجارية: {brand_data["name"]}')

# إنشاء منتجات تجريبية
perfumes_data = [
    {
        'name_ar': 'ديور سوفاج',
        'name_en': 'Dior Sauvage',
        'description_ar': 'عطر رجالي فاخر برائحة خشبية منعشة، مثالي للاستخدام اليومي والمناسبات الخاصة',
        'description_en': 'Luxury men\'s perfume with a refreshing woody scent, perfect for daily use and special occasions',
        'category': 'Men\'s Perfumes',
        'brand': 'Dior',
        'price': 450.00,
        'discount_price': 399.00,
        'size': '100ml',
        'is_featured': True,
        'in_stock': True,
        'stock_quantity': 25,
    },
    {
        'name_ar': 'شانيل رقم 5',
        'name_en': 'Chanel No 5',
        'description_ar': 'العطر الأيقوني الأكثر شهرة في العالم، برائحة زهرية كلاسيكية راقية',
        'description_en': 'The most famous iconic perfume in the world, with a classic elegant floral scent',
        'category': 'Women\'s Perfumes',
        'brand': 'Chanel',
        'price': 550.00,
        'size': '100ml',
        'is_featured': True,
        'in_stock': True,
        'stock_quantity': 15,
    },
    {
        'name_ar': 'فيرساتشي إيروس',
        'name_en': 'Versace Eros',
        'description_ar': 'عطر رجالي قوي وجذاب برائحة منعشة تدوم طويلاً',
        'description_en': 'Strong and attractive men\'s perfume with a long-lasting refreshing scent',
        'category': 'Men\'s Perfumes',
        'brand': 'Versace',
        'price': 380.00,
        'discount_price': 320.00,
        'size': '100ml',
        'is_featured': True,
        'in_stock': True,
        'stock_quantity': 30,
    },
    {
        'name_ar': 'توم فورد بلاك أوركيد',
        'name_en': 'Tom Ford Black Orchid',
        'description_ar': 'عطر فاخر للجنسين برائحة شرقية غامضة وجذابة',
        'description_en': 'Luxury unisex perfume with a mysterious and attractive oriental scent',
        'category': 'Oriental Perfumes',
        'brand': 'Tom Ford',
        'price': 680.00,
        'size': '100ml',
        'is_featured': True,
        'in_stock': True,
        'stock_quantity': 10,
    },
    {
        'name_ar': 'أرماني كود',
        'name_en': 'Armani Code',
        'description_ar': 'عطر رجالي أنيق برائحة خشبية دافئة مثالية للمساء',
        'description_en': 'Elegant men\'s perfume with a warm woody scent perfect for evening',
        'category': 'Men\'s Perfumes',
        'brand': 'Armani',
        'price': 420.00,
        'discount_price': 359.00,
        'size': '75ml',
        'is_featured': False,
        'in_stock': True,
        'stock_quantity': 20,
    },
    {
        'name_ar': 'رصاصي هوكر',
        'name_en': 'Rasasi Hawas',
        'description_ar': 'عطر رجالي منعش برائحة مائية فواكهية مميزة',
        'description_en': 'Refreshing men\'s perfume with a distinctive aquatic fruity scent',
        'category': 'Fresh Perfumes',
        'brand': 'Rasasi',
        'price': 180.00,
        'size': '100ml',
        'is_featured': False,
        'in_stock': True,
        'stock_quantity': 40,
    },
    {
        'name_ar': 'ديور هوم إنتنس',
        'name_en': 'Dior Homme Intense',
        'description_ar': 'عطر رجالي فاخر برائحة زهرية خشبية راقية',
        'description_en': 'Luxury men\'s perfume with an elegant floral woody scent',
        'category': 'Men\'s Perfumes',
        'brand': 'Dior',
        'price': 480.00,
        'size': '100ml',
        'is_featured': True,
        'in_stock': True,
        'stock_quantity': 18,
    },
    {
        'name_ar': 'شانيل كوكو مادموزيل',
        'name_en': 'Chanel Coco Mademoiselle',
        'description_ar': 'عطر نسائي راقي برائحة شرقية زهرية جذابة',
        'description_en': 'Elegant women\'s perfume with an attractive oriental floral scent',
        'category': 'Women\'s Perfumes',
        'brand': 'Chanel',
        'price': 520.00,
        'discount_price': 469.00,
        'size': '100ml',
        'is_featured': True,
        'in_stock': True,
        'stock_quantity': 22,
    },
]

for perfume_data in perfumes_data:
    category = Category.objects.get(name_en=perfume_data['category'])
    brand = Brand.objects.get(name=perfume_data['brand'])
    
    perfume, created = Perfume.objects.get_or_create(
        name_en=perfume_data['name_en'],
        defaults={
            'name_ar': perfume_data['name_ar'],
            'description_ar': perfume_data['description_ar'],
            'description_en': perfume_data['description_en'],
            'category': category,
            'brand': brand,
            'price': perfume_data['price'],
            'discount_price': perfume_data.get('discount_price'),
            'size': perfume_data['size'],
            'is_featured': perfume_data['is_featured'],
            'in_stock': perfume_data['in_stock'],
            'stock_quantity': perfume_data['stock_quantity'],
        }
    )
    if created:
        print(f'✓ تم إنشاء المنتج: {perfume_data["name_ar"]}')

print('\n✅ تم إضافة جميع البيانات التجريبية بنجاح!')
print('\n📝 معلومات تسجيل الدخول:')
print('   Username: admin')
print('   Password: admin123')
print('   Admin URL: http://localhost:8000/admin/')

