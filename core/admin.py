from django.contrib import admin
from cart.models import Cart,OrtherItem
from category.models import Category
from product.models import Product, Comment
from shippingaddress.models import ShippingAddress,PurchaseHistory


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

admin.site.register([Cart,OrtherItem,Product,ShippingAddress,PurchaseHistory,Comment])

admin.site.register(Category, CategoryAdmin)