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

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    WOOD_TYPES = [
        # 🟢 COMMON & AFFORDABLE (Most Popular in Pakistan)
        ('sheesham', 'Sheesham (Indian Rosewood)'),
        ('mango', 'Mango Wood'),
        ('neem', 'Neem Wood'),
        ('acacia', 'Acacia'),
        ('rubberwood', 'Rubberwood'),
        ('babul', 'Babul (Kikar)'),
        ('poplar', 'Poplar'),
        
        # 🟡 MEDIUM RANGE (Good Quality)
        ('deodar', 'Deodar (Himalayan Cedar)'),
        ('chir_pine', 'Chir Pine'),
        ('sandalwood', 'Sandalwood'),
        ('walnut', 'Walnut'),
        ('mahogany', 'Mahogany'),
        
        # 🔴 PREMIUM & LUXURY (Expensive)
        ('teak', 'Teak (Sagwan)'),
        ('rosewood', 'Rosewood (Sheesham Premium)'),
        ('ebony', 'Ebony (Aabnoos)'),
        ('shisham', 'Shisham (Dalbergia Sissoo)'),
        ('partal', 'Partal (Walnut Premium)'),
        
        # 🟣 IMPORTED WOODS (Available in markets)
        ('oak', 'Oak (Imported)'),
        ('maple', 'Maple (Imported)'),
        ('cherry', 'Cherry (Imported)'),
        ('birch', 'Birch (Imported)'),
        ('beech', 'Beech (Imported)'),
        ('sheesham', 'شیشم (Sheesham)'),
        ('kikar', 'کیکر (Kikar)'),
        ('tali', 'تالی (Tali)'),
        ('sufaida', 'سفیدہ (Poplar)'),
        ('shisham', 'شیشم (Shisham)'),
        ('ber', 'بیر (Ber)'),
        ('phalahi', 'پھلاہی (Phalahi)'),
        
        # 🟡 MEDIUM RANGE (معیاری لکڑی)
        ('kail', 'کائل (Kail - Blue Pine)'),
        ('partal', 'پرتل (Partal - Walnut)'),
        ('deodar', 'دیودار (Deodar - Cedar)'),
        ('chir', 'چیر (Chir Pine)'),
        ('marandi', 'مرندی (Marandi)'),
        
        # 🔴 PREMIUM & LUXURY (اعلیٰ معیار)
        ('sohangi', 'سوہانجنا (Sohangi)'),
        ('sandal', 'صندل (Sandalwood)'),
        ('abnus', 'آبنوس (Ebony)'),
        ('rohira', 'روہیڑا (Rohira)'),
        ('saroo', 'سارو (Saroo)'),
        
        # 🟣 FRUIT WOODS (پھل دار درخت)
        ('amrood', 'امرود (Guava Wood)'),
        ('jamun', 'جامن (Java Plum)'),
        ('mango', 'آم (Mango Wood)'),
        ('neem', 'نیم (Neem)'),
        ('akhrot', 'اخروٹ (Walnut)'),
    ]
    PRODUCT_TYPES = [
        ('door', 'Door'),
        ('board', 'Board'),
        ('furniture', 'Furniture'),
        ('craft', 'Handmade Craft'),
        ('accessory', 'Accessory'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=30, choices=PRODUCT_TYPES, default='other')
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

    # New fields for domestic/international sales and export details
    origin_country = models.CharField(max_length=100, blank=True, help_text="Country of origin (e.g. Pakistan)")
    available_domestic = models.BooleanField(default=True)
    available_international = models.BooleanField(default=False)
    export_allowed = models.BooleanField(default=False, help_text="Allow export/sale outside origin country")
    min_order_quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)], help_text="Minimum order quantity")
    lead_time_days = models.IntegerField(default=7, validators=[MinValueValidator(0)], help_text="Lead time in days")
    hs_code = models.CharField(max_length=32, blank=True, help_text="HS / Tariff code for export")
    is_customizable = models.BooleanField(default=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
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
    image = models.ImageField(upload_to='products')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # Category =models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE)
    # name = models.CharField(max_length=250)
    # slug = models.SlugField(max_length=250, unique=True)
    # descreption = models.TextField(blank=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    # available = models.BooleanField(default=True)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    # image = models.ImageField(upload_to='/products', blank=True, null=True)
    
    def __str__(self)-> str:
        return f"Image for {self.product.name}"
    
    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs=[self.product.id, self.product.slug])