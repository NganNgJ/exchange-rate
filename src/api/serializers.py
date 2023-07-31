from django.http import JsonResponse
from api.utils import (
    get_new_datetime
)
from api.models import (
    Currency, Exchangerate,ExchangerateHistory
)
from rest_framework import serializers

class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'


class ExchangerateSerializer(serializers.ModelSerializer):
    start_currency = CurrencySerializer(read_only= True)
    end_currency = CurrencySerializer(read_only= True)
    start_currency_id = serializers.CharField(write_only= True, allow_null= False)
    end_currency_id = serializers.CharField(write_only= True, allow_null= False)

    def create(self, validated_data):
        start_currency_id = validated_data['start_currency_id']
        end_currency_id = validated_data['end_currency_id']
        rate = validated_data['rate']

        if start_currency_id == end_currency_id:
            return JsonResponse({'status' : 'False', 'message': 'The start_currency_id can not be the same as the end_currency_id'})
        if rate == 0: 
            return JsonResponse({'status' : 'False', 'message': 'Rate could not be 0'})
        currency_exchange_rate = Exchangerate.objects.create(start_currency_id = start_currency_id, end_currency_id = end_currency_id, rate = rate, created_at = get_new_datetime())
        return currency_exchange_rate
    
    def update(self, instance, validated_data):
        instance.rate = validated_data.get('rate', instance.rate)
        instance.save()

        start_currency_id = validated_data['start_currency_id']
        end_currency_id = validated_data['end_currency_id']
        new_rate = validated_data['rate']
        
        if start_currency_id == end_currency_id:
            return JsonResponse({'status' : 'False', 'message': 'The start_currency_id can not be the same as the end_currency_id'})
        exchange_rate = Exchangerate.objects.filter(start_currency_id = start_currency_id, end_currency_id = end_currency_id)
        exchange_rate_id = exchange_rate[0].id
        new_history_from_time = exchange_rate[0].created_at
        last_history = ExchangerateHistory.objects.filter(exchange_rate_id = exchange_rate_id).order_by('-from_date').first()
        if last_history is not None:
            new_history_from_time = last_history.end_date
        ExchangerateHistory.objects.create(exchange_rate_id = exchange_rate_id, rate = new_rate, from_date = new_history_from_time ,end_date = get_new_datetime())
        return instance
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


class ExchangerateHistorySerializer(serializers.ModelSerializer):
    from_date = serializers.DateTimeField(allow_null=False)
    # end_date = serializers.DateTimeField(allow_null=False, write_only=True, required=True)
    customer_end_date = serializers.SerializerMethodField(read_only=True)
    exchange_rate = SimpleExchangerateSerializer(many=False)

    def get_customer_end_date(self, obj):
        customer_end_date = None
        if obj.end_date:
            customer_end_date = obj.end_date.strftime('%Y-%m-%d')
        return customer_end_date

    class Meta:
        model = ExchangerateHistory
        fields = '__all__'
        # exclude = ['end_date']



