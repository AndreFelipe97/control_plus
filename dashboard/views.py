from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from sales.models import Sale
from products.models import Product
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from datetime import timedelta

class DashboarSalesSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()

        # Total de vendas de hoje
        total_sales_today = Sale.objects.filter(
            date__date=today
        ).aggregate(total=Sum('total'))['total'] or 0

        # Top 5 produtos mais vendidos
        top_products = Product.objects.annotate(
            total_sales=Sum('saleitem__quantity')
        ).order_by('-total_sales')[:5]

        # Vendas dos últimos 12 meses
        last_12_months = today.replace(day=1) - timedelta(days=365)
        monthly_sales_qs = Sale.objects.filter(date__date__gte=last_12_months).annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total=Sum('total')
        ).order_by('month')

        monthly_sales = [
            {'month': entry['month'].strftime('%Y-%m'), 'total': entry['total']}
            for entry in monthly_sales_qs
        ]

        # Vendas dos últimos 30 dias
        last_30_days = today - timedelta(days=29)
        daily_sales_qs = Sale.objects.filter(date__date__gte=last_30_days).annotate(
            day=TruncDay('date')
        ).values('day').annotate(
            total=Sum('total')
        ).order_by('day')

        daily_sales = [
            {'day': entry['day'].strftime('%Y-%m-%d'), 'total': entry['total']}
            for entry in daily_sales_qs
        ]

        return Response({
            'total_sales_today': total_sales_today,
            'top_products': [
                {
                    'name': p.name,
                    'quantity': p.total_sales or 0
                }
                for p in top_products
            ],
            'monthly_sales': monthly_sales,
            'daily_sales': daily_sales
        })


class DashboarProductsSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_products = Product.objects.count()

        products = Product.objects.all()
        product_data = [
            {
                'name': product.name,
                'stock': product.current_stock,
                'status': 'Estoque baixo' if product.current_stock <= 5 else 'OK'
            }
            for product in products
        ]

        return Response({
            'total_products': total_products,
            'products': product_data
        })
