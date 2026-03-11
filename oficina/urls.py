from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('clientes/', views.clientes, name='clientes'),
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),

    path('equipamentos/', views.equipamentos, name='equipamentos'),
    path('equipamentos/novo/', views.novo_equipamento, name='novo_equipamento'),

    path('ordens/', views.ordens, name='ordens'),
    path('ordens/novo/', views.nova_ordem, name='nova_ordem'),

    path('ordens/finalizar/<int:id>/', views.finalizar_ordem, name='finalizar_ordem'),

    path('ordens/cancelar/<int:id>/', views.cancelar_ordem, name='cancelar_ordem'),

]