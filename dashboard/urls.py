from django.urls import path
from .views import DashboarSalesSummaryView, DashboarProductsSummaryView, ExpenseSummaryView, FinancialReportAPIView, SalesAndStockReportView

urlpatterns = [
    path('dashboard/vendas/', DashboarSalesSummaryView.as_view(), name='dashboard-sales'),
    path('dashboard/produtos/', DashboarProductsSummaryView.as_view(), name='dashboard-products'),
    path('dashboard/despesas/', ExpenseSummaryView.as_view(), name='dashboard-expenses'),
    path('relatorio-financeiro/', FinancialReportAPIView.as_view(), name='dashboard-financial-report'),
    path('relatorios/vendas-estoque/', SalesAndStockReportView.as_view(), name='sales-stock-report')
]
