from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Q
from .models import Perfume, Category, Brand


def home(request):
    """الصفحة الرئيسية"""
    categories = Category.objects.all()[:8]
    featured_perfumes = Perfume.objects.filter(is_featured=True, in_stock=True)[:8]
    
    context = {
        'categories': categories,
        'featured_perfumes': featured_perfumes,
    }
    return render(request, 'home.html', context)


def perfume_list(request):
    """قائمة العطور مع الفلترة"""
    perfumes = Perfume.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    # فلترة حسب الفئة
    category_slug = request.GET.get('category')
    if category_slug:
        perfumes = perfumes.filter(category__slug=category_slug)
    
    # فلترة حسب العلامة التجارية
    brand_id = request.GET.get('brand')
    if brand_id:
        perfumes = perfumes.filter(brand__id=brand_id)
    
    # فلترة حسب السعر
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        perfumes = perfumes.filter(price__gte=min_price)
    if max_price:
        perfumes = perfumes.filter(price__lte=max_price)
    
    # البحث
    query = request.GET.get('q')
    if query:
        perfumes = perfumes.filter(
            Q(name_ar__icontains=query) |
            Q(name_en__icontains=query) |
            Q(description_ar__icontains=query) |
            Q(description_en__icontains=query)
        )
    
    # الترتيب
    sort_by = request.GET.get('sort')
    if sort_by == 'price_low':
        perfumes = perfumes.order_by('price')
    elif sort_by == 'price_high':
        perfumes = perfumes.order_by('-price')
    elif sort_by == 'newest':
        perfumes = perfumes.order_by('-created_at')
    
    context = {
        'perfumes': perfumes,
        'categories': categories,
        'brands': brands,
        'current_category': category_slug,
        'current_brand': brand_id,
    }
    return render(request, 'perfumes/list.html', context)


def perfume_detail(request, slug):
    """تفاصيل العطر"""
    perfume = get_object_or_404(Perfume, slug=slug)
    related_perfumes = Perfume.objects.filter(
        category=perfume.category,
        in_stock=True
    ).exclude(id=perfume.id)[:4]
    
    context = {
        'perfume': perfume,
        'related_perfumes': related_perfumes,
    }
    return render(request, 'perfumes/detail.html', context)
