"""
request/urls.py
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.user_list, name='user_list'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('create-admin/', views.create_admin, name='create_admin'),
]