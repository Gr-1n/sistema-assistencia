from django.urls import path
from . import views
from .views import dashboard

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('clientes/', views.clientes, name='clientes'),
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),

    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),

    path('equipamentos/', views.equipamentos, name='equipamentos'),
    path('equipamentos/novo/', views.novo_equipamento, name='novo_equipamento'),

    path('equipamentos/editar/<int:id>/', views.editar_equipamento, name='editar_equipamento'),
    path('equipamentos/excluir/<int:id>/', views.excluir_equipamento, name='excluir_equipamento'),

    path('ordens/', views.ordens, name='ordens'),
    path('ordens/novo/', views.nova_ordem, name='nova_ordem'),

    path("ordens/editar/<int:id>/", views.editar_ordem, name="editar_ordem"),
    path("ordens/finalizar/<int:id>/", views.finalizar_ordem, name="finalizar_ordem"),
    path("ordens/cancelar/<int:id>/", views.cancelar_ordem, name="cancelar_ordem"),

    path('ordens/status/<int:id>/', views.alterar_status, name='alterar_status'),

    path("ordens/pdf/<int:id>/", views.pdf_ordem, name="pdf_ordem"),

]