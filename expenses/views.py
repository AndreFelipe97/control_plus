from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from .models import Expense, ExpenseCategory
from .serializers import ExpenseSerializer, ExpenseCategorySerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.none()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='mensal-por-categoria')
    def monthly_by_category(self, request):
        today = now().date()
        one_year_ago = today.replace(day=1) - timedelta(days=365)

        qs = self.get_queryset().filter(
            date__gte=one_year_ago
        ).annotate(
            month=TruncMonth('date')
        ).values(
            'month',
            'category__name'
        ).annotate(
            total=Sum('value')
        ).order_by('month', 'category__name')

        result = [
            {
                'month': entry['month'].strftime('%Y-%m'),
                'category': entry['category__name'],
                'total': entry['total']
            }
            for entry in qs
        ]

        return Response(result)


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]


