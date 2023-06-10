from django.http import HttpResponse

from django.http import JsonResponse
from rest_framework.response import Response 
from rest_framework.decorators import api_view
# from rest_framework.views import APIView
from api.models import Task
from django.db.models import Q
import json


# @api_view(['GET'])
# def apiOverview(request):
#     api_urls = {
#         'List': '/task-list/',
#     }
#     return Response(api_urls)

# class ShowAll(APIView):
@api_view(['GET'])
def get_tasks(request):
    filters = Q()

    filter_name = request.GET.get('name', None)
    if filter_name is not None and len(filter_name) > 0:
        filters &= Q(name__contains=filter_name)

    filter_priority = request.GET.get('priority', None)
    if filter_priority is not None and len(filter_priority) > 0 :
        filters &= Q(priority_id=filter_priority)

    queryset = Task.objects.filter(filters)
    data = [{'id': obj.id, 'name': obj.name, 'create_time': obj.create_time, 'status': obj.status} for obj in queryset]
    return JsonResponse({'data': data})