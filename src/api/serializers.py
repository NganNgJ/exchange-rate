from api.models import (
    Currency, Exchangerate
)
from rest_framework import serializers

class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'


class ExchangerateSerializer(serializers.ModelSerializer):
    start_currency = CurrencySerializer()
    end_currency = CurrencySerializer()

    class Meta:
        model = Exchangerate
        fields = '__all__'

        
class SimpleExchangerateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exchangerate
        fields = '__all__'

class CurrencyWithExchangeRatesSerializer(serializers.ModelSerializer):
    exchange_rates = SimpleExchangerateSerializer(many=True, source='start_currency')

    class Meta:
        model = Currency
        fields = '__all__'


