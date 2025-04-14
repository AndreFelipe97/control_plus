from rest_framework.routers import  SimpleRouter
from .views import ProductViewSet, CategoryViewSet, SupplierViewSet, StockMovementViewSet

router = SimpleRouter()
router.register('produtos', ProductViewSet)
router.register('categorias', CategoryViewSet)
router.register('forncedores', SupplierViewSet)
router.register('estoque', StockMovementViewSet)
