from rest_framework.routers import  SimpleRouter
from .views import ProductViewSet, CategoryViewSet

router = SimpleRouter()
router.register('produtos', ProductViewSet)
router.register('categorias', CategoryViewSet)
