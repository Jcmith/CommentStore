from rest_framework import serializers
from request.models import Request
from transactions.models import Money


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ('__all__')


class MoneySerializer(serializers.ModelSerializer):

    class Meta:
        model = Money
        fields = ('__all__')