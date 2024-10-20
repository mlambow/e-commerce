from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets
from django_filters import rest_framework as filter
from rest_framework.exceptions import NotFound
from commerce.serializers import ProductSerializer
from .models import Product, Review
from .serializers import ReviewSerializer, ProductReviewSerializer

#Review Views
#Pagination
class ProductPagination(PageNumberPagination):
    page_size = 5  # Number of products per page
    page_size_query_param = 'page_size'
    max_page_size = 50  # Maximum limit for page size

#creating a review
class SubmitReviewAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#list all the reviews per product id, user id and ratings
class ProductReviewListView(generics.ListAPIView):
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        try:
            product = Product.objects.get(id=product_id)  # This will raise DoesNotExist if the product doesn't exist
            return Review.objects.filter(product=product)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found.", code=status.HTTP_404_NOT_FOUND)

#list all the reviews and reviewer for all the products with product details 
class ProductsReviewListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

#list all users review
class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)