from django.urls import path, include
from .views import (
    ProductRetrieveUpdateDestroyAPIView,
    ProductListView, 
    ProductCreateView, 
    CategoryListCreateView,
    CategoryDetailView,
)

urlpatterns = [
    #Products
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),

    #Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]