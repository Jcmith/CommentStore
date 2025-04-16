from rest_framework import generics
from .serializers import RequestSerializer, MoneySerializer
from transactions.models import Money
from request.models import Request


class MoneyList(generics.ListCreateAPIView):
    serializer_class = MoneySerializer

    def get_queryset(self):
        queryset = Money.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(username=name)
        return queryset


class RequestList(generics.ListCreateAPIView):
    serializer_class = RequestSerializer
    queryset = Request.objects.all()


class MoneyDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MoneySerializer
    queryset = Money.objects.all()


class RequestDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RequestSerializer
    queryset = Request.objects.all()


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ConversionView(APIView):
    # Hard-coded static exchange rates based on GBP (baseline)
    conversion_rates = {
        'GBP': {'GBP': 1.0, 'USD': 1.3, 'EUR': 1.15},
        'USD': {'GBP': 1 / 1.3, 'USD': 1.0, 'EUR': (1 / 1.3) * 1.15},
        'EUR': {'GBP': 1 / 1.15, 'USD': (1 / 1.15) * 1.3, 'EUR': 1.0},
    }

    def get(self, request, currency1, currency2, amount):
        # Validate provided currency codes
        currency1 = currency1.upper()
        currency2 = currency2.upper()
        if currency1 not in self.conversion_rates or currency2 not in self.conversion_rates[currency1]:
            return Response(
                {'error': 'Unsupported currency conversion. Please use GBP, USD, or EUR.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate and convert the amount
        try:
            original_amount = float(amount)
        except ValueError:
            return Response(
                {'error': 'Invalid amount provided. It must be a number.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get conversion rate and calculate converted amount
        rate = self.conversion_rates[currency1][currency2]
        converted_amount = original_amount * rate

        # Construct the response data
        data = {
            'currency1': currency1,
            'currency2': currency2,
            'original_amount': original_amount,
            'converted_amount': converted_amount,
            'rate': rate,
        }
        return Response(data, status=status.HTTP_200_OK)
