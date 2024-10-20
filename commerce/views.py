from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib.auth.models import User
from django_filters import rest_framework as filter
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# Pagination
class ProductPagination(PageNumberPagination):
    page_size = 5  # Number of products per page
    page_size_query_param = 'page_size'
    max_page_size = 50  # Maximum limit for page size

# A class for filters
class ProductFilter(filter.FilterSet):
    min_price = filter.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filter.NumberFilter(field_name='price', lookup_expr='lte')
    category = filter.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']

# A view to retrieve, update and delete the products
class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        details = "Product deleted successfully."
        response_data = {
        'details': details,
        'data': instance.data
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

# A view to list all the products 
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filter.DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = ProductPagination
    search_fields = ['name', 'category__name']

# A view to create the product
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    # A method to handle creation and errors for bad request for product
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            details = "Product successfully created."
            response_data = {
            'details': details,
            'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Category
#category view to list and create categories
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    # A creation override for categories
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)  # Set the created_by field to the current user
        details = "Category successfully created."
        response_data = {
            'details': details,
            'data': serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)  # Return the created category data and status

# A View to retrieve, delete and update your categories 
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    # A deletion method for categories
    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        # only the owner of the category can delete the category
        if category.created_by != request.user:
            return Response({"error": "You do not have permission to delete this category."},
                            status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(category)
        details = "Category successfully deleted."
        response_data = {
            'details': details,
            'data': category.data,
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)