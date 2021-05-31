import datetime
from Reservations.models import Reservation
from Services.models import Station, Service

def check_availability(station, reservation_from, reservation_to):

    availability_list = []
    reservation_list = Reservation.objects.filter(station = station)
    for reservation in reservation_list:
        if reservation.reservation_from > reservation_to or reservation.reservation_to < reservation_from:
            availability_list.append(True)
        else: availability_list.append(False)

    return all(availability_list)