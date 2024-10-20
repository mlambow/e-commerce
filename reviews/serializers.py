from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Review
from commerce.models import Product

# A serializer to show a name of the reviewer in the review
class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

# A serializer to show a product name in the review
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name']

class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserReviewSerializer(read_only=True)
    product_name = ProductSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'product_name', 'user', 'rating', 'review', 'created_at']

# A serializer for the review
class ReviewSerializer(serializers.ModelSerializer):
    user = UserReviewSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'review', 'created_at']

    # A validation to ensure that the rating is between 1 - 5
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Rating must be between 1 and 5')
        return value

    # A validation to ensure that only existing products are reviewed  
    def validate_product(self, value):
        if not Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value