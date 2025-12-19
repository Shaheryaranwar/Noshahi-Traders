from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np


    
def create_realistic_mockup(self, product):
        """Create realistic product mockups"""
        
        # Base template images (you need to download these)
        templates = {
            'tshirt': 'templates/tshirt_template.png',
            'jeans': 'templates/jeans_template.png',
            'shoes': 'templates/shoes_template.png',
            'dress': 'templates/dress_template.png',
            'kurta': 'templates/kurta_template.png',
            'abaya': 'templates/abaya_template.png',
        }
        
        template_file = templates.get(
            self.get_template_type(product.product_type),
            'templates/generic.png'
        )
        
        try:
            # Load template
            template = Image.open(template_file).convert('RGBA')
            
            # Apply color overlay
            color = self.hex_to_rgb(product.color)
            colored = self.apply_color_overlay(template, color)
            
            # Save as product image
            img_io = BytesIO()
            colored.save(img_io, format='PNG', quality=95)
            
            ProductImage.objects.create(
                product=product,
                image=ContentFile(img_io.getvalue(), name=f'mockup_{product.id}.png'),
                alt_text=f"{product.name} - Product Mockup",
                is_primary=True
            )
            
        except Exception as e:
            self.stdout.write(f"Mockup error: {str(e)}")
            # Fallback to download method
            self.download_real_product_images(product)