from django.contrib import admin

# Register your models here.

from .models import (
    Category, Product, Cart, CartItem, Order, OrderItem, HeroSlide,
)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(HeroSlide)

# @admin.register(HeroSlide)
# class HeroSlideAdmin(admin.ModelAdmin):
#     list_display = ("image", "is_active", "order")
#     list_editable = ("is_active", "order")
#     ordering = ("order",)

