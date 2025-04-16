from django.urls import path
from .views import RequestList, RequestDetail, MoneyList, MoneyDetail, ConversionView

urlpatterns = [
    path('request/', RequestList.as_view()),
    path('request/<int:pk>', RequestDetail.as_view()),
    path('money/', MoneyList.as_view()),
    path('money/<int:pk>', MoneyDetail.as_view()),
    path('<str:currency1>/<str:currency2>/<str:amount>/', ConversionView.as_view()),
]