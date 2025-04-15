from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Sale
from products.models import Product
from .serializers import SaleSerializer, SaleItemSerializer

class SaleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        items_data = data.pop('items', [])

        with transaction.atomic():
            sale_serializer = self.get_serializer(data=data)
            sale_serializer.is_valid(raise_exception=True)
            sale = sale_serializer.save()

            total = 0
            for item in items_data:
                item['sale'] = sale.id
                item_serializer = SaleItemSerializer(data=item)
                item_serializer.is_valid(raise_exception=True)
                item_serializer.save()
                total += item['quantity'] * float(item['unit_price'])

                product = Product.objects.get(id=item['product'])
                product.current_stock -= item['quantity']
                product.save()

            sale.total = total
            sale.save()

            response_serializer = self.get_serializer(sale)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
