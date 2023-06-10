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

