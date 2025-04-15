from django.contrib import admin
from .models import Sale, SaleItem

@admin.register(Sale)
class SalesAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'total',
        'payment_method'
    )


@admin.register(SaleItem)
class SaleItems(admin.ModelAdmin):
    list_display = (
        'sale',
        'product',
        'quantity',
        'unit_price'
    )
