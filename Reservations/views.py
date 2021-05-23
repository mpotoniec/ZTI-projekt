from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from Services.models import Service

# Create your views here.
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def index(request):
    #raw_token = request.headers.get('Authorization')
    #raw_token = raw_token.split(' ')
    #token = raw_token[1]

    response = "Dokonaj rezerwacji"

    user = request.user  
    username = user.username
    print(username)

    response = 'Dokonaj rezerwacji' + ' użytkowniku o nazwie: ' + username

    services = ""
    services_list = Service.objects.order_by()
    for service in services_list:
        services += (service.service_name + ', ')

    response = response + " Spis dostępnych usług firmy wulkanizacyjnej: " + services

    #return Response(response + ' użytkowniku o tokenie: ' + token)
    #return Response(response + ' użytkowniku o nazwie: ' + username + ' i tokenie: ' + token)
    return Response(response)