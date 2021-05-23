from django.shortcuts import render
from django.http import HttpResponse
from .models import Service
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def index(request):
    services = ''
    services_list = Service.objects.order_by()
    for service in services_list:
        services += (service.service_name + ', ')

    response = 'Spis dostępnych usług firmy wulkanizacyjnej: ' + services
    return HttpResponse(response)

def information(request, service_name):
    response = ""
    services_list = Service.objects.order_by()
    for service in services_list:
        if service.service_name == service_name:
            response = service.service_information
            break

    return HttpResponse(response)