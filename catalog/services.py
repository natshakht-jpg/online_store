from django.core.cache import cache
from .models import Product, Category


def get_products_by_category(category_id):
    cache_key = f'category_{category_id}'
    products = cache.get(cache_key)

    if products is None:
        try:
            category = Category.objects.get(id=category_id)
            products = Product.objects.filter(category=category)
            cache.set(cache_key, products, 60 * 15)
        except Category.DoesNotExist:
            products = []

    return products

def get_products_from_cache():
    cache_key = 'products_list'
    products = cache.get(cache_key)
    if not products:
        products = Product.objects.all()
        cache.set(cache_key, products, 60 * 15)
    return products