from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reserve/', views.make_reservation, name='make_reservation')
]