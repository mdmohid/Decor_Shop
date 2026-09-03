#myshop urls
from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name="home"),
  path('register/', views.register, name='register'),
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),
  
  path('profile/', views.profile, name='profile'),
  path('products/', views.products, name='products'),
  path(
      'products/<slug:slug>/',
      views.product_detail,
      name='product_detail'
  ),
  path(
      'cart/add/<slug:slug>/',
      views.add_to_cart,
      name='add_to_cart'
  ),
  
  path(
      'cart/',
      views.cart,
      name='cart'
  ),
  path('checkout/', views.checkout, name='checkout'),
  
  path(
      'order-success/<str:order_number>/',
      views.order_success,
      name='order_success'
  ),

]