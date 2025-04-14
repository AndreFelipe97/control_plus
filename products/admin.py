from django.contrib import admin
from .models import Category, Product, Supplier, StockMovement


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


@admin.register(Supplier)
class SuppliersAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'cnpj',
        'phone',
        'email',
        'address',
        'city',
        'state',
        'created_at',
    )


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'supplier',
        'movement_type',
        'quantity',
        'unit_price',
        'date',
        'note',
    )
