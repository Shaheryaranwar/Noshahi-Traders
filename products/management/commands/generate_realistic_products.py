import random
from decimal import Decimal
from django.core.management.base import BaseCommand
<<<<<<< HEAD
from django.core.files.base import ContentFile
from faker import Faker
from io import BytesIO
from PIL import Image, ImageDraw
import os

from products.models import Category, Product, Supplier, ProductImage
=======
from faker import Faker
from products.models import Category, Product, Supplier
>>>>>>> dd4274d184c418728f598078e5ec4137fdd85fcf

fake = Faker()

class Command(BaseCommand):
<<<<<<< HEAD
    help = "Generate products with category-specific images"
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of products to generate'
        )
    
    def handle(self, *args, **kwargs):
        count = kwargs['count']
        
        # Get categories and suppliers
        categories = list(Category.objects.all())
        suppliers = list(Supplier.objects.all())
        
        if not categories:
            self.stdout.write(self.style.ERROR("⚠️ Create categories first in Django admin!"))
            return
        
        if not suppliers:
            # Create a default supplier if none exists
            supplier, created = Supplier.objects.get_or_create(
                name="Default Supplier",
                defaults={
                    'contact_email': 'supplier@example.com',
                    'phone': '0300-1234567',
                    'address': 'Karachi, Pakistan',
                    'country': 'Pakistan'
                }
            )
            suppliers = [supplier]
        
        # Product type mapping
        PRODUCT_TYPE_MAP = {
            'men': ['mens_tshirt', 'mens_shirt', 'mens_jeans', 'mens_trouser', 
                   'mens_kurta', 'mens_shalwar', 'mens_hoodie', 'mens_jacket'],
            'women': ['womens_kurta', 'womens_dress', 'womens_jeans', 'womens_trouser',
                     'womens_blouse', 'womens_abaya', 'womens_skirt'],
            'kids': ['kids_tshirt', 'kids_kurta', 'kids_dress', 'kids_jeans', 
                    'kids_trouser', 'kids_hoodie'],
            
        }
        
        # All available colors from your model
        COLOR_CHOICES = [
            'white', 'black', 'navy_blue', 'sky_blue', 'red', 'green', 
            'yellow', 'pink', 'purple', 'gray', 'brown', 'beige', 
            'maroon', 'olive', 'teal', 'multi'
        ]
        
        for i in range(count):
            try:
                # Select a random category
                category = random.choice(categories)
                category_gender = category.gender
                
                # Select product type based on category gender
                if category_gender in PRODUCT_TYPE_MAP:
                    product_type = random.choice(PRODUCT_TYPE_MAP[category_gender])
                else:
                    # Fallback: combine all types
                    all_types = []
                    for types in PRODUCT_TYPE_MAP.values():
                        all_types.extend(types)
                    product_type = random.choice(all_types)
                
                # ========== CREATE PRODUCT DATA ==========
                # Determine product characteristics
                is_shoes = product_type.endswith('_shoes')
                is_bottom = any(k in product_type for k in ['jeans', 'trouser', 'short', 'skirt'])
                is_upper = not is_shoes and not is_bottom
                
                # Generate name
                color_name = fake.color_name()
                if product_type.startswith('mens_'):
                    gender_prefix = "Men's"
                elif product_type.startswith('womens_'):
                    gender_prefix = "Women's"
                elif product_type.startswith('kids_'):
                    gender_prefix = "Kids"
                else:
                    gender_prefix = "Unisex"
                
                product_type_display = product_type.replace('_', ' ').title()
                name = f"{gender_prefix} {color_name} {product_type_display}"
                slug = f"{product_type.replace('_', '-')}-{color_name.lower()}-{i}"
                
                # Generate price based on product type
                if 'shoes' in product_type:
                    price = Decimal(random.randint(1500, 8000))
                elif 'suit' in product_type or 'blazer' in product_type:
                    price = Decimal(random.randint(5000, 15000))
                elif 'dress' in product_type or 'abaya' in product_type:
                    price = Decimal(random.randint(3000, 10000))
                elif 'kurta' in product_type or 'traditional' in product_type:
                    price = Decimal(random.randint(2000, 7000))
                elif 'jeans' in product_type:
                    price = Decimal(random.randint(2500, 6000))
                else:
                    price = Decimal(random.randint(1000, 5000))
                
                compare_price = price + Decimal(random.randint(500, 2000))
                cost_price = price * Decimal(random.uniform(0.4, 0.7))
                
                # Size logic
                if is_shoes:
                    if 'kids' in product_type:
                        size = random.choice(['28', '30', '32', '34', '36'])
                    else:
                        size = random.choice(['40', '41', '42', '43', '44'])
                elif is_bottom:
                    if 'kids' in product_type:
                        size = random.choice(['2-3y', '4-5y', '6-7y', '8-9y', '10-12y'])
                    elif 'womens' in product_type:
                        size = random.choice(['26', '28', '30', '32', '34'])
                    else:
                        size = random.choice(['30', '32', '34', '36', '38'])
                else:  # upper body
                    if 'kids' in product_type:
                        size = random.choice(['2-3y', '4-5y', '6-7y', '8-9y', '10-12y'])
                    else:
                        size = random.choice(['xs', 's', 'm', 'l', 'xl'])
                
                # Fabric logic
                fabric_choices = {
                    'kids': ['cotton', 'poly_cotton', 'terry_cotton'],
                    'traditional': ['khadar', 'cotton', 'silk_cotton'],
                    'formal': ['cotton', 'linen', 'viscose'],
                    'winter': ['fleece', 'corduroy'],
                    'default': ['cotton', 'linen', 'viscose']
                }
                
                fabric = 'cotton'  # default
                if not is_shoes:
                    if 'kids' in product_type:
                        fabric = random.choice(fabric_choices['kids'])
                    elif any(k in product_type for k in ['kurta', 'traditional', 'shalwar', 'abaya']):
                        fabric = random.choice(fabric_choices['traditional'])
                    elif any(k in product_type for k in ['shirt', 'blouse', 'suit', 'blazer']):
                        fabric = random.choice(fabric_choices['formal'])
                    elif any(k in product_type for k in ['hoodie', 'sweater', 'jacket', 'coat']):
                        fabric = random.choice(fabric_choices['winter'])
                    else:
                        fabric = random.choice(fabric_choices['default'])
                
                # Color selection
                color = random.choice(COLOR_CHOICES)
                
                # Measurements
                length = None
                chest_width = None
                waist_width = None
                shoulder_width = None
                
                if is_upper:
                    if 'kids' in product_type:
                        length = Decimal(round(random.uniform(20, 30), 2))
                        chest_width = Decimal(round(random.uniform(12, 18), 2))
                        shoulder_width = Decimal(round(random.uniform(10, 14), 2))
                    else:
                        length = Decimal(round(random.uniform(26, 42), 2))
                        chest_width = Decimal(round(random.uniform(18, 24), 2))
                        shoulder_width = Decimal(round(random.uniform(14, 18), 2))
                elif is_bottom:
                    if 'kids' in product_type:
                        length = Decimal(round(random.uniform(24, 36), 2))
                        waist_width = Decimal(round(random.uniform(20, 28), 2))
                    else:
                        length = Decimal(round(random.uniform(36, 44), 2))
                        waist_width = Decimal(round(random.uniform(30, 38), 2))
                
                # ========== CREATE PRODUCT IN DATABASE ==========
                product = Product.objects.create(
=======
    help = "Generate 500 realistic products with proper category-type matching"

    def handle(self, *args, **kwargs):
        categories = list(Category.objects.all())
        suppliers = list(Supplier.objects.all())

        if not categories or not suppliers:
            self.stdout.write(self.style.ERROR("Create categories and suppliers first"))
            return

        # Define product types by gender/category
        PRODUCT_TYPE_MAP = {
            'men': [
                'mens_tshirt', 'mens_shirt', 'mens_trouser', 'mens_jeans',
                'mens_kurta', 'mens_shalwar', 'mens_waistcoat', 'mens_blazer',
                'mens_suit', 'mens_hoodie', 'mens_jacket', 'mens_coat',
                'mens_short', 'mens_shoes', 'mens_sweater'
            ],
            'women': [
                'womens_kurta', 'womens_suit', 'womens_dress', 'womens_abaya',
                'womens_hoodie', 'womens_trouser', 'womens_jeans', 'womens_blouse',
                'womens_shawl', 'womens_jacket', 'womens_coat', 'womens_skirt',
                'womens_sweater', 'womens_shoes'
            ],
            'kids': [
                'kids_kurta', 'kids_tshirt', 'kids_trouser', 'kids_dress',
                'kids_traditional', 'kids_jeans', 'kids_hoodie', 'kids_jacket',
                'kids_coat', 'kids_shoes'
            ],
            'unisex': [
                'unisex_hoodie', 'unisex_tshirt', 'unisex_tracksuit'
            ]
        }

        for i in range(500):
            # Step 1: Randomly select a category
            category = random.choice(categories)
            
            # Step 2: Get gender from category
            category_gender = category.gender  # 'men', 'women', 'kids', 'unisex'
            
            # Step 3: Select product type based on category gender
            if category_gender in PRODUCT_TYPE_MAP:
                product_type = random.choice(PRODUCT_TYPE_MAP[category_gender])
            else:
                # Fallback to any product type
                all_types = []
                for types in PRODUCT_TYPE_MAP.values():
                    all_types.extend(types)
                product_type = random.choice(all_types)

            # -------- TYPE DETECTION --------
            is_shoes = product_type.endswith('_shoes')
            is_bottom = any(k in product_type for k in ['jeans','trouser','short','skirt'])
            is_upper = not is_shoes and not is_bottom

            # -------- BASIC DATA --------
            # Create a more realistic name
            if product_type.startswith('mens_'):
                gender_prefix = "Men's"
            elif product_type.startswith('womens_'):
                gender_prefix = "Women's"
            elif product_type.startswith('kids_'):
                gender_prefix = "Kids"
            else:
                gender_prefix = "Unisex"
            
            product_name_map = {
                'mens_tshirt': 'T-Shirt',
                'womens_tshirt': 'T-Shirt',
                'kids_tshirt': 'T-Shirt',
                'unisex_tshirt': 'T-Shirt',
                'mens_shirt': 'Shirt',
                'womens_blouse': 'Blouse',
                'mens_jeans': 'Jeans',
                'womens_jeans': 'Jeans',
                'kids_jeans': 'Jeans',
                'mens_trouser': 'Trousers',
                'womens_trouser': 'Trousers',
                'kids_trouser': 'Trousers',
                'mens_kurta': 'Kurta',
                'womens_kurta': 'Kurti',
                'kids_kurta': 'Kurta',
                'womens_dress': 'Dress',
                'kids_dress': 'Dress',
                'womens_abaya': 'Abaya',
                'mens_shalwar': 'Shalwar Kameez',
                'kids_traditional': 'Traditional Wear',
                'mens_hoodie': 'Hoodie',
                'womens_hoodie': 'Hoodie',
                'kids_hoodie': 'Hoodie',
                'unisex_hoodie': 'Hoodie',
                'mens_jacket': 'Jacket',
                'womens_jacket': 'Jacket',
                'kids_jacket': 'Jacket',
                'mens_coat': 'Coat',
                'womens_coat': 'Coat',
                'kids_coat': 'Coat',
                'mens_short': 'Shorts',
                'womens_skirt': 'Skirt',
                'mens_shoes': 'Shoes',
                'womens_shoes': 'Shoes',
                'kids_shoes': 'Shoes',
                'mens_sweater': 'Sweater',
                'womens_sweater': 'Sweater',
                'mens_suit': 'Suit',
                'womens_suit': 'Suit',
                'mens_waistcoat': 'Waistcoat',
                'womens_shawl': 'Shawl',
                'mens_blazer': 'Blazer',
                'unisex_tracksuit': 'Tracksuit',
            }
            
            product_display_name = product_name_map.get(product_type, product_type.replace('_', ' ').title())
            name = f"{gender_prefix} {fake.color_name()} {product_display_name}"
            slug = f"{product_type.replace('_', '-')}-{fake.word()}-{i}".lower()

            # -------- PRICING LOGIC --------
            # Different price ranges for different product types
            if 'shoes' in product_type:
                price = Decimal(random.randint(1500, 8000))
            elif 'suit' in product_type or 'blazer' in product_type:
                price = Decimal(random.randint(5000, 15000))
            elif 'dress' in product_type or 'abaya' in product_type:
                price = Decimal(random.randint(3000, 10000))
            elif 'kurta' in product_type or 'traditional' in product_type:
                price = Decimal(random.randint(2000, 7000))
            elif 'jeans' in product_type:
                price = Decimal(random.randint(2500, 6000))
            else:
                price = Decimal(random.randint(1000, 5000))
            
            compare_price = price + Decimal(random.randint(500, 2000))
            cost_price = price * Decimal(random.uniform(0.4, 0.7))

            # -------- SIZE LOGIC --------
            if is_shoes:
                if 'kids' in product_type:
                    size = random.choice(['28','30','32','34','36'])
                else:
                    size = random.choice(['40','41','42','43','44','45'])
            elif is_bottom:
                if 'kids' in product_type:
                    size = random.choice(['2-3y','4-5y','6-7y','8-9y','10-12y'])
                elif 'womens' in product_type:
                    size = random.choice(['26','28','30','32','34'])
                else:  # mens/unisex
                    size = random.choice(['30','32','34','36','38','40'])
            else:  # upper body
                if 'kids' in product_type:
                    size = random.choice(['2-3y','4-5y','6-7y','8-9y','10-12y'])
                else:
                    size = random.choice(['xs','s','m','l','xl','xxl'])

            # -------- FABRIC LOGIC --------
            fabric_choices = {
                'shoes': None,
                'kids': ['cotton', 'poly_cotton', 'terry_cotton'],
                'traditional': ['khadar', 'cotton', 'silk_cotton', 'embroidered'],
                'formal': ['cotton', 'linen', 'viscose'],
                'casual': ['cotton', 'jersey', 'poly_cotton'],
                'winter': ['fleece', 'wool', 'corduroy'],
                'default': ['cotton', 'linen', 'viscose', 'poly_cotton']
            }
            
            fabric = None
            if not is_shoes:
                if 'kids' in product_type:
                    fabric = random.choice(fabric_choices['kids'])
                elif any(k in product_type for k in ['kurta', 'traditional', 'shalwar', 'abaya']):
                    fabric = random.choice(fabric_choices['traditional'])
                elif any(k in product_type for k in ['shirt', 'blouse', 'suit', 'blazer']):
                    fabric = random.choice(fabric_choices['formal'])
                elif any(k in product_type for k in ['hoodie', 'sweater', 'jacket', 'coat']):
                    fabric = random.choice(fabric_choices['winter'])
                else:
                    fabric = random.choice(fabric_choices['default'])

            # -------- MEASUREMENTS --------
            measurements = {
                'length': None,
                'chest_width': None,
                'waist_width': None,
                'shoulder_width': None,
            }

            if is_upper:
                if 'kids' in product_type:
                    measurements.update({
                        'length': random.uniform(20, 30),
                        'chest_width': random.uniform(12, 18),
                        'shoulder_width': random.uniform(10, 14),
                    })
                else:
                    measurements.update({
                        'length': random.uniform(26, 42),
                        'chest_width': random.uniform(18, 24),
                        'shoulder_width': random.uniform(14, 18),
                    })

            elif is_bottom:
                if 'kids' in product_type:
                    measurements.update({
                        'length': random.uniform(24, 36),
                        'waist_width': random.uniform(20, 28),
                    })
                else:
                    measurements.update({
                        'length': random.uniform(36, 44),
                        'waist_width': random.uniform(30, 38),
                    })

            # -------- COLOR LOGIC --------
            # Gender/type specific colors
            if 'kids' in product_type:
                color_choices = ['red', 'yellow', 'green', 'blue', 'pink', 'multi']
            elif any(k in product_type for k in ['kurta', 'traditional', 'shalwar', 'abaya']):
                color_choices = ['white', 'navy_blue', 'maroon', 'green', 'beige', 'multi']
            elif any(k in product_type for k in ['shirt', 'blouse', 'suit', 'blazer']):
                color_choices = ['white', 'black', 'navy_blue', 'gray', 'beige']
            else:
                color_choices = [c[0] for c in Product.COLOR_CHOICES]
            
            color = random.choice(color_choices)

            # -------- CARE INSTRUCTIONS --------
            care_map = {
                'cotton': 'Machine wash cold, tumble dry low',
                'linen': 'Hand wash recommended, line dry',
                'silk': 'Dry clean only',
                'denim': 'Wash inside out with similar colors',
                'wool': 'Dry clean or hand wash in cold water',
                'poly_cotton': 'Machine wash warm, tumble dry medium',
                'khadar': 'Hand wash separately, air dry',
            }
            
            care = care_map.get(fabric, 'Follow care label instructions')

            # -------- SEASON LOGIC --------
            if any(k in product_type for k in ['hoodie', 'sweater', 'jacket', 'coat']):
                season = 'winter'
            elif any(k in product_type for k in ['kurta', 'shalwar', 'traditional']):
                season = random.choice(['all_season', 'summer', 'spring'])
            else:
                season = random.choice(['summer', 'winter', 'all_season', 'spring', 'autumn'])

            # -------- OCCASION LOGIC --------
            if any(k in product_type for k in ['suit', 'blazer', 'shirt']):
                occasion = 'formal'
            elif any(k in product_type for k in ['dress', 'abaya', 'kurta', 'traditional']):
                occasion = random.choice(['wedding', 'eid', 'party'])
            elif any(k in product_type for k in ['jeans', 'tshirt', 'hoodie']):
                occasion = 'casual'
            else:
                occasion = random.choice(['casual', 'formal', 'party', 'everyday'])

            # -------- CREATE PRODUCT --------
            try:
                Product.objects.create(
>>>>>>> dd4274d184c418728f598078e5ec4137fdd85fcf
                    name=name,
                    slug=slug,
                    description=fake.paragraph(nb_sentences=3),
                    category=category,
                    product_type=product_type,
                    fabric_type=fabric,
                    size=size,
                    color=color,
                    price=price,
                    compare_price=compare_price,
                    cost_price=cost_price,
                    sku=f"SKU-{product_type[:3].upper()}-{fake.unique.bothify(text='#####')}",
                    stock_quantity=random.randint(5, 150),
                    is_active=True,
                    is_featured=random.choice([True, False]),
<<<<<<< HEAD
                    length=length,
                    chest_width=chest_width,
                    waist_width=waist_width,
                    shoulder_width=shoulder_width,
                    care_instructions="Machine wash cold, tumble dry low",
                    season=random.choice(['summer', 'winter', 'all_season']),
                    occasion=random.choice(['casual', 'formal', 'party']),
=======
                    care_instructions=care,
                    season=season,
                    occasion=occasion,
>>>>>>> dd4274d184c418728f598078e5ec4137fdd85fcf
                    origin_country="Pakistan",
                    available_domestic=True,
                    available_international=random.choice([True, False]),
                    export_allowed=random.choice([True, False]),
                    min_order_quantity=1,
                    lead_time_days=random.choice([2, 3, 5, 7]),
<<<<<<< HEAD
                    supplier=random.choice(suppliers) if suppliers else None,
                )
                
                # ========== GENERATE IMAGES FOR THIS PRODUCT ==========
                # self.generate_smart_product_images(product)
                
                self.stdout.write(f"✅ Created product: {name}")
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"❌ Error creating product {i}: {str(e)}"))
                continue
        
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Successfully generated {count} products with images!"))
    
    # ========== IMAGE GENERATION METHODS (KEEP THESE AS IS) ==========
    
    def generate_smart_product_images(self, product):
        """Generate accurate images based on product type and category"""
        
        # Map product types to specific image generators
        image_generators = {
            # MEN'S CLOTHING
            'mens_tshirt': self.generate_tshirt_image,
            'mens_shirt': self.generate_shirt_image,
            'mens_jeans': self.generate_jeans_image,
            'mens_trouser': self.generate_trouser_image,
            'mens_kurta': self.generate_kurta_image,
            'mens_shalwar': self.generate_shalwar_image,
            'mens_suit': self.generate_suit_image,
            'mens_hoodie': self.generate_hoodie_image,
            'mens_jacket': self.generate_jacket_image,
            'mens_shoes': self.generate_shoes_image,
            
            # WOMEN'S CLOTHING
            'womens_kurta': self.generate_womens_kurta_image,
            'womens_dress': self.generate_dress_image,
            'womens_jeans': self.generate_womens_jeans_image,
            'womens_abaya': self.generate_abaya_image,
            'womens_blouse': self.generate_blouse_image,
            'womens_skirt': self.generate_skirt_image,
            
            # KIDS CLOTHING
            'kids_tshirt': self.generate_kids_tshirt_image,
            'kids_kurta': self.generate_kids_kurta_image,
            'kids_dress': self.generate_kids_dress_image,
            'kids_jeans': self.generate_kids_jeans_image,
        }
        
        # Get the appropriate image generator
        generator = image_generators.get(
            product.product_type, 
            self.generate_generic_clothing_image  # Fallback
        )
        
        # Generate 2-4 images for this product
        num_images = random.randint(2, 4)
        for img_num in range(num_images):
            img_type = ['front', 'back', 'detail', 'texture'][img_num] if img_num < 4 else 'detail'
            
            try:
                # Generate the specific image
                image_content = generator(product, view=img_type)
                
                # Create ProductImage
                product_image = ProductImage(
                    product=product,
                    alt_text=f"{product.name} - {img_type.title()} View",
                    is_primary=(img_num == 0),
                    color_variant=product.color if img_num > 1 else ''
                )
                
                # Save image
                img_name = f"{product.product_type}_{product.color}_{img_type}_{random.randint(1000,9999)}.jpg"
                product_image.image.save(img_name, image_content, save=True)
                
            except Exception as e:
                self.stdout.write(f"⚠️ Image error for {product.product_type}: {str(e)}")
                # Create a simple fallback image
                self.create_fallback_image(product)
    
    def generate_tshirt_image(self, product, view="front"):
        """Generate accurate T-Shirt image"""
        img = Image.new('RGB', (800, 1000), self.get_color_rgb('white'))
        draw = ImageDraw.Draw(img)
        
        # T-Shirt shape
        color = self.get_color_rgb(product.color)
        
        # Body
        draw.rectangle([200, 200, 600, 800], fill=color, outline=(0,0,0), width=3)
        
        # Neck
        draw.ellipse([350, 150, 450, 250], fill='white', outline=(0,0,0), width=3)
        
        # Sleeves
        draw.rectangle([100, 250, 200, 500], fill=color, outline=(0,0,0), width=3)  # Left
        draw.rectangle([600, 250, 700, 500], fill=color, outline=(0,0,0), width=3)  # Right
        
        return self.image_to_contentfile(img)
    
    def generate_shirt_image(self, product, view="front"):
        """Generate Formal Shirt image"""
        img = Image.new('RGB', (800, 1000), self.get_color_rgb('white'))
        draw = ImageDraw.Draw(img)
        
        color = self.get_color_rgb(product.color)
        
        # Shirt body
        draw.polygon([(200, 200), (600, 200), (550, 800), (250, 800)], 
                    fill=color, outline=(0,0,0), width=3)
        
        # Collar
        draw.polygon([(350, 150), (450, 150), (500, 200), (300, 200)], 
                    fill=color, outline=(0,0,0), width=2)
        
        # Buttons
        for i, y in enumerate(range(250, 750, 80)):
            draw.ellipse([380, y, 420, y+40], fill='white', outline=(0,0,0), width=2)
        
        # Pocket for front view
        if view == "front":
            draw.rectangle([500, 300, 580, 380], fill=color, outline=(0,0,0), width=2)
        
        return self.image_to_contentfile(img)
    
    def generate_jeans_image(self, product, view="front"):
        """Generate Jeans image"""
        img = Image.new('RGB', (800, 1000), self.get_color_rgb('white'))
        draw = ImageDraw.Draw(img)
        
        # Jeans color (blue variants)
        if product.color in ['navy_blue', 'blue', 'sky_blue']:
            color = self.get_color_rgb(product.color)
        else:
            color = (21, 96, 189)  # Default jeans blue
        
        # Pants shape
        # Waist
        draw.rectangle([250, 200, 550, 300], fill=color, outline=(0,0,0), width=3)
        
        # Legs
        draw.rectangle([250, 300, 400, 900], fill=color, outline=(0,0,0), width=3)  # Left
        draw.rectangle([400, 300, 550, 900], fill=color, outline=(0,0,0), width=3)  # Right
        
        # Belt loops
        for x in range(280, 551, 40):
            draw.rectangle([x, 200, x+20, 230], fill=(139, 69, 19), outline=(0,0,0), width=1)
        
        return self.image_to_contentfile(img)
    
    def generate_kurta_image(self, product, view="front"):
        """Generate Men's Kurta image"""
        img = Image.new('RGB', (800, 1200), self.get_color_rgb('white'))
        draw = ImageDraw.Draw(img)
        
        color = self.get_color_rgb(product.color)
        
        # Kurta body (long)
        draw.rectangle([200, 150, 600, 1000], fill=color, outline=(0,0,0), width=3)
        
        # Neck (round for kurta)
        draw.ellipse([350, 100, 450, 200], fill=color, outline=(0,0,0), width=3)
        
        # Side slits
        draw.line([200, 800, 150, 1100], fill=color, width=3)
        draw.line([600, 800, 650, 1100], fill=color, width=3)
        
        # Buttons/Placket
        draw.rectangle([395, 200, 405, 400], fill=(255,255,255), outline=(0,0,0), width=2)
        for y in range(220, 401, 30):
            draw.ellipse([398, y, 402, y+10], fill='gold', outline=(0,0,0), width=1)
        
        return self.image_to_contentfile(img)
    
    def generate_shoes_image(self, product, view="front"):
        """Generate Shoes image"""
        img = Image.new('RGB', (1000, 800), self.get_color_rgb('white'))
        draw = ImageDraw.Draw(img)
        
        color = self.get_color_rgb(product.color)
        
        # Left shoe
        shoe_points = [
            (200, 400), (400, 300), (600, 350), 
            (550, 600), (300, 550), (200, 400)
        ]
        draw.polygon(shoe_points, fill=color, outline=(0,0,0), width=3)
        
        # Right shoe (offset)
        shoe_points_right = [(x+350, y) for x, y in shoe_points]
        draw.polygon(shoe_points_right, fill=color, outline=(0,0,0), width=3)
        
        # Shoelaces
        for i in range(5):
            y = 450 + i*30
            draw.line([300, y, 500, y], fill='white', width=3)  # Left
            draw.line([650, y, 850, y], fill='white', width=3)  # Right
        
        return self.image_to_contentfile(img)
    
    def generate_dress_image(self, product, view="front"):
        """Generate Women's Dress image"""
        img = Image.new('RGB', (800, 1200), self.get_color_rgb('white'))
        draw = ImageDraw.Draw(img)
        
        color = self.get_color_rgb(product.color)
        
        # Dress silhouette (A-line)
        dress_points = [
            (350, 150), (450, 150),  # Shoulders
            (500, 400), (550, 800),  # Right side
            (250, 800), (300, 400),  # Left side
            (350, 150)  # Close
        ]
        draw.polygon(dress_points, fill=color, outline=(0,0,0), width=3)
        
        # Neckline
        draw.arc([330, 130, 470, 200], 0, 180, fill='black', width=3)
        
        # Waist emphasis
        draw.line([350, 350, 450, 350], fill=(255,255,255), width=2)
        
        return self.image_to_contentfile(img)
    
    def generate_abaya_image(self, product, view="front"):
        """Generate Abaya image"""
        img = Image.new('RGB', (600, 1200), self.get_color_rgb('white'))
        draw = ImageDraw.Draw(img)
        
        # Abaya is usually black, but can be other colors
        if product.color == 'black':
            color = (0, 0, 0)
        else:
            color = self.get_color_rgb(product.color)
        
        # Abaya shape (flowing)
        draw.rectangle([100, 100, 500, 1100], fill=color, outline=(100,100,100), width=2)
        
        # Head opening
        draw.ellipse([250, 80, 350, 180], fill=color, outline=(100,100,100), width=2)
        
        # Sleeves
        draw.rectangle([50, 200, 100, 500], fill=color, outline=(100,100,100), width=2)  # Left
        draw.rectangle([500, 200, 550, 500], fill=color, outline=(100,100,100), width=2)  # Right
        
        return self.image_to_contentfile(img)
    
    def generate_kids_tshirt_image(self, product, view="front"):
        """Generate Kids T-Shirt (smaller)"""
        img = Image.new('RGB', (600, 800), self.get_color_rgb('white'))
        draw = ImageDraw.Draw(img)
        
        color = self.get_color_rgb(product.color)
        
        # Smaller body for kids
        draw.rectangle([150, 150, 450, 600], fill=color, outline=(0,0,0), width=2)
        
        # Neck
        draw.ellipse([250, 100, 350, 200], fill='white', outline=(0,0,0), width=2)
        
        # Sleeves
        draw.rectangle([80, 200, 150, 400], fill=color, outline=(0,0,0), width=2)  # Left
        draw.rectangle([450, 200, 520, 400], fill=color, outline=(0,0,0), width=2)  # Right
        
        return self.image_to_contentfile(img)
    
    def generate_generic_clothing_image(self, product, view="front"):
        """Fallback generator for unspecified product types"""
        img = Image.new('RGB', (800, 1000), self.get_color_rgb('white'))
        draw = ImageDraw.Draw(img)
        
        color = self.get_color_rgb(product.color)
        
        # Generic clothing shape
        draw.rectangle([200, 200, 600, 800], fill=color, outline=(0,0,0), width=3)
        
        return self.image_to_contentfile(img)
    
    def generate_womens_kurta_image(self, product, view="front"):
        """Women's Kurta is similar to men's but can be styled differently"""
        return self.generate_kurta_image(product, view)
    
    def generate_womens_jeans_image(self, product, view="front"):
        """Women's Jeans might be more fitted"""
        return self.generate_jeans_image(product, view)
    
    def generate_trouser_image(self, product, view="front"):
        """Trousers image"""
        return self.generate_jeans_image(product, view)  # Similar shape
    
    def generate_shalwar_image(self, product, view="front"):
        """Shalwar Kameez image"""
        return self.generate_kurta_image(product, view)  # Similar to kurta
    
    def generate_suit_image(self, product, view="front"):
        """Suit image"""
        return self.generate_shirt_image(product, view)  # Similar to formal shirt
    
    def generate_hoodie_image(self, product, view="front"):
        """Hoodie image"""
        img = Image.new('RGB', (800, 1000), self.get_color_rgb('white'))
        draw = ImageDraw.Draw(img)
        
        color = self.get_color_rgb(product.color)
        
        # Hoodie body (similar to t-shirt but with hood)
        draw.rectangle([200, 200, 600, 800], fill=color, outline=(0,0,0), width=3)
        
        # Hood
        draw.arc([300, 100, 500, 250], 0, 180, fill=color, outline=(0,0,0), width=3)
        
        # Sleeves
        draw.rectangle([100, 250, 200, 500], fill=color, outline=(0,0,0), width=3)  # Left
        draw.rectangle([600, 250, 700, 500], fill=color, outline=(0,0,0), width=3)  # Right
        
        # Pocket
        draw.rectangle([300, 600, 500, 700], fill=color, outline=(0,0,0), width=2)
        
        return self.image_to_contentfile(img)
    
    def generate_jacket_image(self, product, view="front"):
        """Jacket image"""
        return self.generate_hoodie_image(product, view)  # Similar to hoodie
    
    def generate_blouse_image(self, product, view="front"):
        """Blouse image"""
        return self.generate_shirt_image(product, view)  # Similar to shirt
    
    def generate_skirt_image(self, product, view="front"):
        """Skirt image"""
        img = Image.new('RGB', (800, 1000), self.get_color_rgb('white'))
        draw = ImageDraw.Draw(img)
        
        color = self.get_color_rgb(product.color)
        
        # Skirt shape (A-line)
        draw.polygon([(300, 200), (500, 200), (600, 800), (200, 800)], 
                    fill=color, outline=(0,0,0), width=3)
        
        return self.image_to_contentfile(img)
    
    def generate_kids_dress_image(self, product, view="front"):
        """Kids Dress image"""
        return self.generate_dress_image(product, view)  # Similar to women's dress
    
    def generate_kids_kurta_image(self, product, view="front"):
        """Kids Kurta image"""
        return self.generate_kurta_image(product, view)  # Similar to kurta
    
    def generate_kids_jeans_image(self, product, view="front"):
        """Kids Jeans image"""
        return self.generate_jeans_image(product, view)  # Similar to jeans
    
    def create_fallback_image(self, product):
        """Create a simple color block as fallback"""
        img = Image.new('RGB', (800, 800), self.get_color_rgb(product.color))
        content = self.image_to_contentfile(img)
        
        ProductImage.objects.create(
            product=product,
            image=ContentFile(content.getvalue(), name=f'fallback_{product.id}.jpg'),
            alt_text=f"{product.name} - Product Image",
            is_primary=True
        )
    
    # ==================== HELPER METHODS ====================
    
    def get_color_rgb(self, color_name):
        """Convert color name to RGB"""
        color_map = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 128, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'pink': (255, 192, 203),
            'purple': (128, 0, 128),
            'navy_blue': (0, 0, 128),
            'sky_blue': (135, 206, 235),
            'gray': (128, 128, 128),
            'grey': (128, 128, 128),
            'brown': (165, 42, 42),
            'beige': (245, 245, 220),
            'maroon': (128, 0, 0),
            'olive': (128, 128, 0),
            'teal': (0, 128, 128),
            'multi': random.choice([(255,0,0), (0,255,0), (0,0,255)]),
        }
        
        if color_name not in color_map:
            # Generate random color
            return (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        
        return color_map[color_name]
    
    def image_to_contentfile(self, image):
        """Convert PIL Image to Django ContentFile"""
        img_io = BytesIO()
        image.save(img_io, format='JPEG', quality=90)
        img_io.seek(0)
        return ContentFile(img_io.getvalue())
=======
                    supplier=random.choice(suppliers),
                    **measurements
                )
                
                if i % 50 == 0:
                    self.stdout.write(f"Created {i} products...")
                    
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error creating product {i}: {str(e)}"))
                continue

        self.stdout.write(self.style.SUCCESS("✅ 500 realistic products generated with proper category-type matching"))
>>>>>>> dd4274d184c418728f598078e5ec4137fdd85fcf
