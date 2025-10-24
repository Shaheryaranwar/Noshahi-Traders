from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm

@login_required
def checkout(request):
    cart_id = Cart.get_cart_id(request)
    cart = get_object_or_404(Cart, id=cart_id)
    
    if cart.items.count() == 0:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')
    
    # Check stock availability
    for item in cart.items.all():
        if item.quantity > item.product.stock_quantity:
            messages.error(request, f'Sorry, only {item.product.stock_quantity} items of {item.product.name} are available.')
            return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            
            # Calculate totals
            subtotal = cart.total_price
            tax_amount = subtotal * 0.1  # 10% tax
            shipping_cost = 10.00  # Fixed shipping cost
            total_amount = subtotal + tax_amount + shipping_cost
            
            order.subtotal = subtotal
            order.tax_amount = tax_amount
            order.shipping_cost = shipping_cost
            order.total_amount = total_amount
            order.save()
            
            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                
                # Update product stock
                product = cart_item.product
                product.stock_quantity -= cart_item.quantity
                product.save()
            
            # Clear the cart
            cart.items.all().delete()
            
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('orders:order_confirmation', order_number=order.order_number)
    else:
        # Pre-populate form with user data
        initial_data = {
            'shipping_full_name': f"{request.user.first_name} {request.user.last_name}",
            'shipping_address': request.user.address,
            'shipping_city': request.user.city,
            'shipping_state': request.user.state,
            'shipping_zip_code': request.user.zip_code,
            'shipping_country': request.user.country,
            'shipping_phone': request.user.phone,
            'billing_full_name': f"{request.user.first_name} {request.user.last_name}",
            'billing_address': request.user.address,
            'billing_city': request.user.city,
            'billing_state': request.user.state,
            'billing_zip_code': request.user.zip_code,
            'billing_country': request.user.country,
        }
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart': cart,
    }
    return render(request, 'orders/checkout.html', context)