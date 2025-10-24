from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = Cart.get_cart_id(request)
    cart = get_object_or_404(Cart, id=cart_id)
    
    if product.stock_quantity == 0:
        messages.error(request, 'Sorry, this product is out of stock.')
        return redirect('products:product_detail', slug=product.slug)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        if cart_item.quantity < product.stock_quantity:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'Updated {product.name} quantity in your cart.')
        else:
            messages.error(request, f'Only {product.stock_quantity} items available in stock.')
    else:
        messages.success(request, f'Added {product.name} to your cart.')
    
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart_id = Cart.get_cart_id(request)
    cart = get_object_or_404(Cart, id=cart_id)
    
    context = {
        'cart': cart,
    }
    return render(request, 'cart/cart_detail.html', context)