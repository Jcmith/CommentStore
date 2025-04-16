from django.urls import path
from .views import PaymentList, PaymentDetail, MoneyList, MoneyDetail, ConversionView

urlpatterns = [
    path('payment/', PaymentList.as_view()),
    path('payment/<int:pk>', PaymentDetail.as_view()),
    path('money/', MoneyList.as_view()),
    path('money/<int:pk>', MoneyDetail.as_view()),
    path('<str:currency1>/<str:currency2>/<str:amount>/', ConversionView.as_view()),
]