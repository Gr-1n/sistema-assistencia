from django.contrib import admin
from .models import Cliente, Equipamento, OrdemServico

admin.site.register(Cliente)
admin.site.register(Equipamento)
admin.site.register(OrdemServico)
