from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
]
