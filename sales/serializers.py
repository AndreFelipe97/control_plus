from rest_framework import serializers
from .models import Sale, SaleItem
from products.serializers import ProductSerializer


class SaleItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleItem
        fields = (
            'id',
            'sale',
            'product',
            'quantity',
            'unit_price'
        )


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = (
            'id',
            'date',
            'total',
            'payment_method',
            'items'
        )
        read_only_fields = ['id', 'date', 'total']
