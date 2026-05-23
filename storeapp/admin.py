from django.contrib import admin

# Register your models here.

from .models import Category, Product, Cart, CategoryOffer

admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(Product)
admin.site.register(CategoryOffer)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_percentage', 'category')
    list_editable = ('discount_percentage',)

admin.site.register(Cart)
