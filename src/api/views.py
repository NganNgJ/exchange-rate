from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response 
from rest_framework.decorators import api_view
# from rest_framework.views import APIView
from api.models import (
    Currency,
    Exchangerate,
    ExchangerateHistory,
)
from django.db.models import Q
import json


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

#Currency
@api_view(['GET'])
def get_all_currency(request):
    filters = Q()
    currencies = Currency.objects.filter(filters)
    data = [{'id': obj.id, 'name': obj.name, 'symbol': obj.symbol, 'status': obj.status} for obj in currencies]    
    return JsonResponse({'data':data})

@api_view(['POST'])
def create_currency(request):
    name = request.data.get('name')
    symbol = request.data.get('symbol')
    new_currency = Currency.objects.create(name = name, symbol = symbol)
    return JsonResponse({'data': {'id': new_currency.id, 'name': new_currency.name, 'symbol': new_currency.symbol, 'status': new_currency.status}})

@api_view(['POST'])
def adjust_currency(request):
    adjust_id = request.data.get('id')
    new_name = request.data.get('new_name')
    new_symbol = request.data.get('new_symbol')
    Currency.objects.filter(id = adjust_id).update(name = new_name, symbol = new_symbol)
    update_currency = Currency.objects.get(id = adjust_id)
    return JsonResponse({'data': {'id': update_currency.id, 'name': update_currency.name, 'symbol': update_currency.symbol, 'status': update_currency.status}})

#Exchange rate
@api_view(['GET'])
def get_all_exchange_rate(request):
    filters = Q()
    exchange_rates = Exchangerate.objects.filter(filters)
    currency_ids = list(set([rate.start_currency.id for rate in exchange_rates] + [rate.end_currency.id for rate in exchange_rates]))
    currencies = Currency.objects.filter(id__in=currency_ids)
    currency_name_dict = {currency.id: currency.symbol for currency in currencies}
    data = [{'id': obj.id, 
             'start_currency_id': obj.start_currency.id,
             'start_currency_symbol': currency_name_dict[obj.start_currency.id],
             'end_currency_id': obj.end_currency.id,
             'end_currency_symbol': currency_name_dict[obj.end_currency.id],
             'rate': obj.rate} for obj in exchange_rates]    
    return JsonResponse({'data':data})


@api_view(['POST'])
def create_exchange_rate(request):
    start_currency_id = Currency.objects.get(id = request.data.get('start_currency_id'))
    end_currency_id = Currency.objects.get(id = request.data.get('end_currency_id'))
    rate = request.data.get('rate')
    if start_currency_id == end_currency_id:
        return JsonResponse({'status' : 'False', 'message': 'The start_currency_id can not be the same as the end_currency_id'})
    currency_exchange_rate = Exchangerate.objects.create(start_currency = start_currency_id, end_currency = end_currency_id, rate = rate )
    return JsonResponse({'data': {'id': currency_exchange_rate.id,
                                   'start_currency_id': currency_exchange_rate.start_currency.id,
                                   'end_currency_id': currency_exchange_rate.end_currency.id,
                                   'rate': currency_exchange_rate.rate}})

@api_view(['POST'])
def calculate_exchange_rate(request):
    start_currency_cal = Currency.objects.get(symbol = request.data.get('start_currency'))
    end_currency_cal = Currency.objects.get(symbol = request.data.get('end_currency'))
    exchange_amount = request.data.get('amount_to_exchange')
    exchange_data = Exchangerate.objects.filter(
                                        (Q(start_currency = start_currency_cal) | Q(end_currency = start_currency_cal)) & 
                                        (Q(start_currency = end_currency_cal) | Q(end_currency = end_currency_cal))).first()
    if exchange_data:
        if start_currency_cal.id == exchange_data.start_currency.id:
            rate = exchange_data.rate
        elif start_currency_cal.id == exchange_data.end_currency.id:
            rate = 1/(exchange_data.rate)
    else:
        rate = None 
    if rate is not None:
        result = { 'start_currency': start_currency_cal.symbol,
                   'end_currency': end_currency_cal.symbol,
                    'rate': rate,
                    'exchange_amount': exchange_amount,
                    'result_amount': exchange_amount * rate
                }
    else: 
        result = {'message': 'No exchange rate found for the given currencies.'}
    
    return JsonResponse({'data': result})



