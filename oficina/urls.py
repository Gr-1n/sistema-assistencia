from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('clientes/', views.clientes, name='clientes'),

    path('equipamentos/', views.equipamentos, name='equipamentos'),

    path('ordens/', views.ordens, name='ordens'),

]