from .models import Category
from django.core.cache import cache

def category_menu(request):
    tree = cache.get('category_menu_tree')
    if tree is None:
        tree = Category.get_menu_tree()
        cache.set('category_menu_tree', tree, 60 * 15)
    return {'menu_categories': tree}