from rest_framework import serializers
from .models import Product, Category, Supplier, StockMovement


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'name'
        )


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'category_id',
            'purchase_price',
            'selling_price',
            'unit_measurement',
            'barcode',
            'current_stock',
        )


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = (
            'id',
            'name',
            'cnpj',
            'phone',
            'email',
            'address',
            'city',
            'state',
            'created_at',
        )


class StockMovementSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockMovement
        fields = (
            'id',
            'product',
            'supplier',
            'movement_type',
            'quantity',
            'unit_price',
            'date',
            'note',
        )
