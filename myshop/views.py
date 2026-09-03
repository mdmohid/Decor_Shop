from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product
from uuid import uuid4
from .models import  Cart, CartItem, Order, OrderItem

# Create your views here.
#home
def home(request):
  return render(request,'index.html')

#products
# def products(request):
#     return render(request, 'products.html')

# def products(request):
#     products = Product.objects.all()

#     return render(request, 'products.html', {
#         'products': products
#     })

def products(request):
    products = Product.objects.filter(is_available=True)

    return render(request, 'products.html', {
        'products': products
    })

#product detail
def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        is_available=True
    )

    return render(request, 'product_detail.html', {
        'product': product
    })


#register
def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'register.html')

#login
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('profile')  #instead of home (i.e home)

        messages.error(request, 'Invalid username or password.')
        return redirect('login')

    return render(request, 'login.html')

#logout
def logout_view(request):

    logout(request)
    return redirect('home')
  
  
#profile
@login_required
def profile(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'profile.html', {
        'orders': orders
    })


#add to cart
@login_required
def add_to_cart(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        is_available=True
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1

    cart_item.save()

    return redirect('cart')
  
#cart
@login_required
def cart(request):
  
      cart, created = Cart.objects.get_or_create(
          user=request.user
      )
  
      cart_items = cart.items.select_related('product')
  
      total = sum(
          item.product.price * item.quantity
          for item in cart_items
      )
  
      return render(request, 'cart.html', {
          'cart': cart,
          'cart_items': cart_items,
          'total': total
      })
      
      
      
#checkout view
@login_required
def checkout(request):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_items = cart.items.select_related('product')

    if not cart_items.exists():
        return redirect('cart')

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    if request.method == 'POST':

        shipping_address = request.POST.get('shipping_address')
        phone = request.POST.get('phone')

        order = Order.objects.create(
            user=request.user,
            order_number=f"ORD-{uuid4().hex[:8].upper()}",
            shipping_address=shipping_address,
            phone=phone,
            total_amount=total
        )

        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart.items.all().delete()

        return redirect(
            'order_success',
            order_number=order.order_number
        )

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })
    
#order success
@login_required
def order_success(request, order_number):

    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user
    )

    return render(request, 'order_success.html', {
        'order': order
    })