# accounts/urls.py
from django.urls import path
from .views import LoginView

urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
]
