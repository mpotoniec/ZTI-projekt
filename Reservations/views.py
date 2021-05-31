from django.db.models.fields import DateTimeField
from django.shortcuts import render
from django.http import HttpResponse, response
from django.views.decorators.csrf import requires_csrf_token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from Services.models import Service, Station
from .models import Reservation

import datetime

# Create your views here.
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def index(request):
    
    reservation = Reservation.objects.filter(user = request.user)
    if not reservation: return Response('Nie posiadasz żadnej rezerwacji')
    else: 
        response = 'Twoja rezerwacja to: '

        this_reservation = reservation.order_by()
        service_id = this_reservation[0].service_id
        station_id = this_reservation[0].station_id
        from_ = this_reservation[0].reservation_from
        to_ = this_reservation[0].reservation_to

        service = Service.objects.filter(id = service_id)
        this_service = service.order_by()
        station = Station.objects.filter(id = station_id)
        this_station = station.order_by()

        this_service_name = this_service[0].service_name
        this_station_number = this_station[0].station_number

        response += this_service_name + (' termin od ') + str(from_) + (' termin do ') + str(to_) + ' na stanowsku nr: ' + str(this_station_number)

        return Response(response)

        
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def make_reservation(request):

    print(request.user)
    print(request.user.username)
    print(request.body)
    reservation_data = request.body
    print(type(reservation_data))
    print(reservation_data[4])

    '''now = datetime.datetime.now()

    new_reservation = Reservation()
    new_reservation.user = request.user

    service = Service.objects.filter(service_name = 'Wymiana Opon')
    new_reservation.service = service[0]
    station = Station.objects.filter(station_number = 1)
    new_reservation.station = station[0]

    new_reservation.reservation_from = now
    new_reservation.reservation_to = now

    new_reservation.save()'''

    response = 'Dokonano rezerwacji'

    return Response(response)