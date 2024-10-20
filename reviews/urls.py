from django.urls import path, include
from .views import ProductReviewListView, SubmitReviewAPIView, UserReviewListView, ProductsReviewListView

#Review urls
urlpatterns = [
    path('product/<int:product_id>/reviews/', ProductReviewListView.as_view(), name='product-review'),
    path('reviews/', SubmitReviewAPIView.as_view(), name='create-review'),
    path('users/reviews/', UserReviewListView.as_view(), name='users-review'),
    path('products/reviews/', ProductsReviewListView.as_view(), name='products_reviews'),
]