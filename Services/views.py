from django.shortcuts import render
from django.http import HttpResponse, response
from django.urls.conf import path
from .models import Service, Station
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def index(request):
    services = ''
    services_list = Service.objects.order_by()
    for service in services_list:
        services += (service.service_name + ', ')
        services += (service.service_information + ', ')
        services += (service.service_cost + ', ')
        services += (service.service_duration + '. ')

    #response = services
    response = ''
    for i in range(len(services) - 1):
        if i == len(services) - 2:
            break
        response+=services[i]
    return Response(response)

@api_view(['GET'])
def get_services_and_stations(request):
    response = ''
    
    services = ''
    services_list = Service.objects.order_by()
    for service in services_list:
        services += (service.service_name + '-')

    stations = ''
    stations_list = Station.objects.order_by()
    for station in stations_list:
        stations += (str(station.station_number) + '-') 

    output_services = ''
    for i in range(len(services) - 1):
        if i == len(services) - 1: break
        output_services += services[i]

    output_stations = ''
    for i in range(len(stations) - 1):
        if i == len(stations) - 1: break
        output_stations += stations[i]

    output_services += '|'
    response = output_services + output_stations

    return Response(response)