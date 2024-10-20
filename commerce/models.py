from django.db import models
from django.contrib.auth.models import  User
from django.utils import timezone
from .manager import CustomUserManager

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, related_name='category', on_delete=models.CASCADE, default=2)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    #created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)

    def reduce_stock(self, quantity):
        if quantity > self.stock_quantity:
            raise ValueError("Not enough stock available.")
        self.stock_quantity -= quantity
        self.save()

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)