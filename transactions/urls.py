"""
transactions/urls.py
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.money_transfer, name='money_transfer'),
]
