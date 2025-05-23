"""
URL configuration for control_plus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from products.urls import router as products_router
from sales.urls import router as sales_router
from expenses.urls import router as expenses_router

api_v1_patterns = [
    path('', include(products_router.urls)),
    path('', include(sales_router.urls)),
    path('', include(expenses_router.urls)),
    path('', include('dashboard.urls')),
    path('', include('accounts.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('api/v1/', include(api_v1_patterns)),
]
