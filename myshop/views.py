from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Product

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
            return redirect('home')

        messages.error(request, 'Invalid username or password.')
        return redirect('login')

    return render(request, 'login.html')

#logout
def logout_view(request):

    logout(request)
    return redirect('home')

