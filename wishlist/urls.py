from django.urls import path
from .views import WishlistCreate, WishlistList, WishlistRetrieveDestroy, WishlistItemCreate, WishlistItemList, WishlistItemRetrieveDestroy

urlpatterns = [
    path('wishlists/create/', WishlistCreate.as_view(), name='wishlist-list-create'),
    path('wishlists/', WishlistList.as_view(), name='wishlist-list-create'),
    path('wishlists/<int:pk>/', WishlistRetrieveDestroy.as_view(), name='wishlist-detail'),  # To retrieve and delete
    path('wishlist-items/create/', WishlistItemCreate.as_view(), name='wishlist-item-list-create'),
    path('wishlist-items/', WishlistItemList.as_view(), name='wishlistitems'),
    path('wishlist-items/<int:pk>/', WishlistItemRetrieveDestroy.as_view(), name='wishlist-item-detail'),  # To retrieve and delete
]