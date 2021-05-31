from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getinfo/', views.get_services_and_stations, name='get_services_and_stations'),
]