from django import template
from shop.models import Product

register = template.Library()


@register.inclusion_tag("include/related_products.html")
def show_related_products(product, limit=8):

    category_ids = product.category.get_descendant_ids()

    products = (
        Product.objects
        .select_related("category")
        .filter(
            category_id__in=category_ids,
            is_available=True
        )
        .exclude(pk=product.pk)
        .order_by("-created_at")[:limit]
    )

    return {
        "r_products": products
    }