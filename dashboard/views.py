from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from sales.models import Sale, SaleItem
from products.models import Product
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Sum, F, DecimalField, ExpressionWrapper

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


class Expense:
    pass


class ExpenseSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = now().date()
        last_30_days = today - timedelta(days=30)
        one_year_ago = today.replace(day=1) - timedelta(days=365)

        # Total dos últimos 30 dias
        total_last_30_days = Expense.objects.filter(
            user=request.user,
            date__gte=last_30_days
        ).aggregate(total=Sum('value'))['total'] or 0

        # Totais por categoria dos últimos 30 dias
        category_summary = Expense.objects.filter(
            user=request.user,
            date__gte=last_30_days
        ).values('category__name').annotate(
            total=Sum('value')
        ).order_by('-total')

        # Totais mensais dos últimos 12 meses
        monthly_summary_qs = Expense.objects.filter(
            user=request.user,
            date__gte=one_year_ago
        ).annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total=Sum('value')
        ).order_by('month')

        monthly_summary = [
            {
                'month': entry['month'].strftime('%Y-%m'),
                'total': entry['total']
            }
            for entry in monthly_summary_qs
        ]

        return Response({
            'total_last_30_days': total_last_30_days,
            'by_category_last_30_days': category_summary,
            'monthly_summary_last_12_months': monthly_summary
        })


class FinancialReportAPIView(APIView):
    def get(self, request):
        hoje = timezone.now().date()
        primeiro_dia = hoje.replace(day=1)
        ano_atual = hoje.year

        # Total de vendas no mês atual
        vendas = Sale.objects.filter(data__gte=primeiro_dia).aggregate(total=Sum('valor'))['total'] or 0

        # Total de despesas no mês atual
        despesas = Expense.objects.filter(data__gte=primeiro_dia).aggregate(total=Sum('valor'))['total'] or 0

        # Lucro líquido
        lucro_liquido = vendas - despesas

        # Margem de lucro líquida (%)
        margem_liquida = (lucro_liquido / vendas * 100) if vendas else 0

        return Response({
            'vendas': vendas,
            'despesas': despesas,
            'lucro_liquido': lucro_liquido,
            'margem_liquida': round(margem_liquida, 2)
        })


class SalesAndStockReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filtros opcionais
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not start_date or not end_date:
            end_date = now().date()
            start_date = end_date - timedelta(days=30)  # padrão: últimos 30 dias

        # Itens vendidos no período
        items = SaleItem.objects.filter(
            sale__date__range=[start_date, end_date]
        ).select_related('product')

        sales_summary = items.values(
            'product__name'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(ExpressionWrapper(F('quantity') * F('unit_price'), output_field=DecimalField())),
        ).order_by('-total_quantity')

        # Estoque atual
        stock_summary = Product.objects.all().values(
            'name',
            'current_stock'
        ).order_by('current_stock')

        return Response({
            'period': {
                'start_date': str(start_date),
                'end_date': str(end_date)
            },
            'sales_summary': list(sales_summary),
            'stock_summary': list(stock_summary)
        })
