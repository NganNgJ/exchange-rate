from django.http import HttpResponse

# def hello(request):
#     return HttpResponse("Hello world")
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from api.models import Tasks


# @api_view(['GET'])
# def apiOverview(request):
#     api_urls = {
#         'List': '/task-list/',
#     }
#     return Response(api_urls)

# class ShowAll(APIView):
def index(request):
    queryset = Tasks.objects.all()
    data = [{'id': obj.id, 'name': obj.name} for obj in queryset]
    return HttpResponse(data)