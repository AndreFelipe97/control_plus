from rest_framework.routers import SimpleRouter
from .views import ExpenseViewSet, ExpenseCategoryViewSet


router = SimpleRouter()
router.register('despesas', ExpenseViewSet)
router.register('categoria-despesa', ExpenseCategoryViewSet)
