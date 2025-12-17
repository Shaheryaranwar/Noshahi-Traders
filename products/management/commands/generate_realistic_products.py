import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from faker import Faker
from products.models import Category, Product, Supplier

fake = Faker()

class Command(BaseCommand):
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
                    care_instructions=care,
                    season=season,
                    occasion=occasion,
                    origin_country="Pakistan",
                    available_domestic=True,
                    available_international=random.choice([True, False]),
                    export_allowed=random.choice([True, False]),
                    min_order_quantity=1,
                    lead_time_days=random.choice([2, 3, 5, 7]),
                    supplier=random.choice(suppliers),
                    **measurements
                )
                
                if i % 50 == 0:
                    self.stdout.write(f"Created {i} products...")
                    
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error creating product {i}: {str(e)}"))
                continue

        self.stdout.write(self.style.SUCCESS("✅ 500 realistic products generated with proper category-type matching"))