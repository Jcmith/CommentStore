"""
request/urls.py
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.superuser_home, name='superuser_home'),
    path('users/', views.user_list, name='user_list'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('create-superuser/', views.create_superuser, name='create_superuser'),
]