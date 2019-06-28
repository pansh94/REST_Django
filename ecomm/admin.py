from django.contrib import admin

from .models import Product, ShoppingCart


class ShoppingCartAdmin(admin.ModelAdmin):
    fields = ['name', 'address']


class ProductAdmin(admin.ModelAdmin):
    fields = ['name','price','description','start_sale','end_sale']
    list_display = ('name', 'price', 'is_on_sale')


admin.site.register(Product, ProductAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
