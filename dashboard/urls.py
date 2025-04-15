from django.urls import path
from .views import DashboarSalesSummaryView, DashboarProductsSummaryView


urlpatterns = [
    path('dashboard/vendas/', DashboarSalesSummaryView.as_view(), name='dashboard-sales'),
    path('dashboard/produtos/', DashboarProductsSummaryView.as_view(), name='dashboard-products')
]
