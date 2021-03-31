from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:service_name>/', views.information, name='information'),
]