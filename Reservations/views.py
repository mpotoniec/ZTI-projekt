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

from Reservations.Reservation_Functions.availability import check_availability

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

    months = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12,
    }

    reservation_data = request.body
    reservation_data = reservation_data.decode('utf-8')
    reservation_data = reservation_data.split('-')

    reservation_data_service = ''
    for element in reservation_data[0]:
        if element != '"': reservation_data_service += element

    reservation_data_station = ''
    for element in reservation_data[1]:
        if element != '"': reservation_data_station += element
    reservation_data_station = int(reservation_data_station)

    reservation_data_date = ''
    for element in reservation_data[2]:
        if element != '"': reservation_data_date += element

    reservation_data_date = reservation_data_date.split(' ')

    if reservation_data_date[0] == 'Sun': return Response('Niestety nie można dokonać rezerwacji w tym dniu.')    

    reservation_data_date_day = int(reservation_data_date[2])
    reservation_data_date_month = reservation_data_date[1]
    reservation_data_date_year = int(reservation_data_date[3])
    reservation_data_date_hour_min_sec = reservation_data_date[4]

    reservation_data_date_month = months[reservation_data_date_month]
    reservation_data_date_hour_min_sec = reservation_data_date_hour_min_sec.split(':')
    reservation_data_date_hour_start = int(reservation_data_date_hour_min_sec[0])
    reservation_data_date_min_start = int(reservation_data_date_hour_min_sec[1])
    reservation_data_date_sec = int(reservation_data_date_hour_min_sec[2])

    if reservation_data_date_hour_start < 8:
        return Response('Zbyt wczesna godzina rezerwacji. Można rezerwaować najwcześniej od godziny 8:00')

    service = Service.objects.filter(service_name = reservation_data_service)
    station = Station.objects.filter(station_number = reservation_data_station)

    duration = service[0].service_duration
    duration = duration.split()
    hour_to_add = ''
    for element in duration[0]:
        if element.isdigit(): hour_to_add += element
    hour_to_add = int(hour_to_add)
    
    min_to_add = ''
    if len(duration) > 1:
        for element in duration[1]:
            if element.isdigit(): min_to_add += element
        min_to_add = int(min_to_add)
    else:
        min_to_add = 0


    reservation_data_date_hour_stop = reservation_data_date_hour_start + hour_to_add
    reservation_data_date_min_stop = reservation_data_date_min_start + min_to_add

    if reservation_data_date_hour_stop > 20: 
        return Response('Czas trwania rezerwacji przekracza godziny pracy zakładu. Pracujemy pn-sb do godziny 20.')
    elif reservation_data_date_hour_stop == 20 and reservation_data_date_min_stop > 0:
        return Response('Czas trwania rezerwacji przekracza godziny pracy zakładu. Pracujemy pn-sb do godziny 20.')

    if reservation_data_date_min_stop >= 60:
        reservation_data_date_hour_stop+=1
        reservation_data_date_min_stop = reservation_data_date_min_stop - 60

    reservation_date_start = datetime.datetime(
        reservation_data_date_year,
        reservation_data_date_month,
        reservation_data_date_day,
        reservation_data_date_hour_start,
        reservation_data_date_min_start,
        reservation_data_date_sec
    )

    reservation_date_stop = datetime.datetime(
        reservation_data_date_year,
        reservation_data_date_month,
        reservation_data_date_day,
        reservation_data_date_hour_stop,
        reservation_data_date_min_stop,
        reservation_data_date_sec
    )

    if check_availability(station[0], reservation_date_start, reservation_date_stop) == False:
        print('Brak rezerwacji')
        return Response('Ten termin rezerwacji jest już zajęty. Spróbuj zarezerwować o innej godzinie')

    print('Rezerwacja')


    new_reservation = Reservation()
    new_reservation.user = request.user
    new_reservation.service = service[0]
    new_reservation.station = station[0]
    new_reservation.reservation_from = reservation_date_start
    new_reservation.reservation_to = reservation_date_stop

    new_reservation.save()

    return Response('Dokonano rezerwacji')