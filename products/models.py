from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:category_detail', args=[self.slug])

class Product(models.Model):
    WOOD_TYPES = [
        ('oak', 'Oak'),
        ('teak', 'Teak'),
        ('mahogany', 'Mahogany'),
        ('walnut', 'Walnut'),
        ('pine', 'Pine'),
        ('maple', 'Maple'),
        ('cherry', 'Cherry'),
        ('birch', 'Birch'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    wood_type = models.CharField(max_length=20, choices=WOOD_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sku = models.CharField(max_length=50, unique=True)
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Dimensions
    length = models.DecimalField(max_digits=6, decimal_places=2, help_text="Length in inches")
    width = models.DecimalField(max_digits=6, decimal_places=2, help_text="Width in inches")
    height = models.DecimalField(max_digits=6, decimal_places=2, help_text="Height in inches")
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="Weight in pounds")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])
    
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    def get_discount_percentage(self):
        if self.compare_price and self.compare_price > self.price:
            return int(((self.compare_price - self.price) / self.compare_price) * 100)
        return 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.product.name}"