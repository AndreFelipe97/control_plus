from rest_framework.routers import SimpleRouter
from .views import SaleViewSet


router = SimpleRouter()
router.register('vendas', SaleViewSet)
