from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category_id',
        'purchase_price',
        'selling_price',
        'unit_measurement',
        'barcode',
        'current_stock'
    )
