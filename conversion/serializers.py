from rest_framework import serializers
from commentstoreapp.models import Payment
from transactions.models import Money


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ('__all__')


class MoneySerializer(serializers.ModelSerializer):

    class Meta:
        model = Money
        fields = ('__all__')