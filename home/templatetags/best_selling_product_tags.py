from django import template
from shop.models import Product, Category

register = template.Library()

@register.inclusion_tag('include/best_sellers_product.html')
def show_best_selling_products():
    best_sellers = Product.objects.filter(is_bestseller=True).order_by('-created_at')[:6]

    return {'best_sellers': best_sellers}


@register.inclusion_tag('include/new_product.html')
def show_new_products():
    new_product = Product.objects.filter(is_new=True).order_by('-created_at')[:6]

    return {'new_product': new_product}


@register.inclusion_tag('include/show_category_in_index.html')
def show_category_in_index():
    categories = Category.objects.filter(
        is_active=True,
        parent__isnull=True
    ).order_by('-created_at')[:12]

    return {'categories': categories}