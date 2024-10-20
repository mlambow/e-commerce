from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wishlist, WishlistItem
from commerce.models import Product

# A serializer to show a product name in the review
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name']

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'name']

class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = ['id', 'wishlist', 'product','product_id', 'added_at']