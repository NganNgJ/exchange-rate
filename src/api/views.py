from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import viewsets
# from rest_framework.views import APIView
from api.models import (
    Currency,
    Exchangerate,
    ExchangerateHistory,
)
from api.serializers import (
    CurrencySerializer,
    CurrencyWithExchangeRatesSerializer,
    ExchangerateSerializer,
    SimpleExchangerateSerializer,
    ExchangerateHistorySerializer
)
from api.utils import (
    get_new_datetime
)
from django.db.models import Q
import json
import datetime
from django.utils import timezone
import pytz

# @api_view(['GET'])
# def get_tasks(request):
#     filters = Q()

#     filter_name = request.GET.get('name', None)
#     if filter_name is not None and len(filter_name) > 0:
#         filters &= Q(name__contains=filter_name)

#     filter_priority = request.GET.get('priority', None)
#     if filter_priority is not None and len(filter_priority) > 0 :
#         filters &= Q(priority_id=filter_priority)

#     queryset = Task.objects.filter(filters)
#     # first_task = queryset.first()
#     # prio_name = first_task.priority.name
#     data = [{'id': obj.id, 'name': obj.name, 'create_time': obj.create_time, 'status': obj.status} for obj in queryset]
#     return JsonResponse({'data': data})

class CurrencyViewSet(viewsets.ModelViewSet):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all().order_by('-id')

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class ExchangerateHistoryViewset(viewsets.ModelViewSet):
    serializer_class = ExchangerateHistorySerializer
    queryset = ExchangerateHistory.objects.all().order_by('-id')


class ExchangerateViewset(viewsets.ModelViewSet):
    serializer_class = ExchangerateSerializer
    queryset = Exchangerate.objects.all().order_by('-id')




#Currency
@api_view(['GET'])
def get_all_currency(request):
    filters = Q()
    currencies = Currency.objects.filter(filters)
    return JsonResponse({'data': CurrencyWithExchangeRatesSerializer(currencies, many=True).data})

@api_view(['POST'])
def create_currency(request):
    name = request.data.get('name')
    symbol = request.data.get('symbol')
    new_currency = Currency.objects.create(name = name, symbol = symbol)
    return JsonResponse({'data': CurrencySerializer(new_currency).data})

@api_view(['POST'])
def adjust_currency(request):
    adjust_id = request.data.get('id')
    new_name = request.data.get('new_name')
    new_symbol = request.data.get('new_symbol')
    Currency.objects.filter(id = adjust_id).update(name = new_name, symbol = new_symbol)
    update_currency = Currency.objects.get(id = adjust_id)
    return JsonResponse({'data': CurrencySerializer(update_currency).data})

#Exchange rate
@api_view(['GET'])
def get_all_exchange_rate(request):
    filters = Q()
    exchange_rates = Exchangerate.objects.filter(filters)
    currency_ids = list(set([rate.start_currency.id for rate in exchange_rates] + [rate.end_currency.id for rate in exchange_rates]))
    currencies = Currency.objects.filter(id__in=currency_ids)
    currency_name_dict = {currency.id: currency.symbol for currency in currencies}

    # data = []
    # for exchange_rate in exchange_rates:
    #     data.append(
    #         {
    #             'id': exchange_rate.id, 
    #             'start_currency': CurrencySerializer(exchange_rate.start_currency).data,
    #             'end_currency': CurrencySerializer(exchange_rate.end_currency).data,
    #             'rate': exchange_rate.rate,
    #             'last_updated_time': exchange_rate.created_at
    #          }
    #     )
    return JsonResponse({'data': ExchangerateSerializer(exchange_rates, many=True).data})



@api_view(['POST'])
def create_exchange_rate(request):
    start_currency_id = request.data.get('start_currency_id')
    start_currency = Currency.objects.get(id = start_currency_id)
    if start_currency is None:
        return JsonResponse({'message': 'No exchange rate found for the given currencies.'})
    
    end_currency_id = request.data.get('end_currency_id')
    end_currency = Currency.objects.get(id = end_currency_id)
    if end_currency is None:
        return JsonResponse({'message': 'No exchange rate found for the given currencies.'})
    
    rate = request.data.get('rate')

    if start_currency_id == end_currency_id:
        return JsonResponse({'status' : 'False', 'message': 'The start_currency_id can not be the same as the end_currency_id'})
    currency_exchange_rate = Exchangerate.objects.create(start_currency = start_currency, end_currency = end_currency, rate = rate, created_at = get_new_datetime())

    # return JsonResponse(
    #     {
    #         'data': {
    #             'id': currency_exchange_rate.id,
    #             'start_currency_id': currency_exchange_rate.start_currency_id,
    #             'end_currency_id': currency_exchange_rate.end_currency_id,
    #             'rate': currency_exchange_rate.rate,
    #             'created_at': currency_exchange_rate.created_at
    #         }
    #     }
    # )
    return JsonResponse({'data': SimpleExchangerateSerializer(currency_exchange_rate).data})

@api_view(['PUT'])
def adjust_exchange_rate(request):
    exchange_rate_id = request.data.get('exchange_rate_id')
    exchange_rate = Exchangerate.objects.get(id = exchange_rate_id)
    if exchange_rate is None: 
        return JsonResponse({'status' : 'False', 'message': 'This exchange currency does not exist'})
    new_rate = request.data.get('new_rate')
    if new_rate is None: 
        return JsonResponse({'status' : 'False', 'message': 'The new rate is none'})
    new_history_from_time = exchange_rate.created_at
    last_history = ExchangerateHistory.objects.filter(exchange_rate_id = exchange_rate.id).order_by('-from_date').first()
    if last_history is not None:
        new_history_from_time = last_history.end_date
    ExchangerateHistory.objects.create(exchange_rate_id = exchange_rate.id, rate = new_rate, from_date = new_history_from_time ,end_date = get_new_datetime())
    exchange_rate.rate = new_rate
    exchange_rate.save()

    return JsonResponse(
        {
            'data': {
                'id': exchange_rate.id,
                'new_rate': new_rate
        }
    })
    


@api_view(['GET'])
def calculate_exchange_rate(request):
    exchange_id = request.GET.get('exchange_id')
    exchange_rate = Exchangerate.objects.get(id = exchange_id)
    if exchange_rate is None: 
        return JsonResponse({'status' : 'False', 'message': 'This exchange currency does not exist'})
    exchange_amount = request.GET.get('amount_to_exchange')
    exchange_amount = float(exchange_amount)
    is_revert = request.GET.get('is_revert')
                                        
    if exchange_rate is None:
        return JsonResponse({'message': 'No exchange rate found for the given currencies.'})
    rate = exchange_rate.rate if is_revert == '0' else 1 / (exchange_rate.rate)
    result = {  
                'rate': rate,
                'result_amount': exchange_amount * rate
            }
    
    return JsonResponse({'data': result})
    
