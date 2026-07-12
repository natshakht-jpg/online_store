from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'catalog'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('category/<int:category_id>/', views.CategoryProductsView.as_view(), name='category_products'),
]
