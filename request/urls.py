"""
request/urls.py
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.new_request, name='request'),
]
