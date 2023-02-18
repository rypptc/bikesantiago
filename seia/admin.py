from django.contrib import admin
from .models import Proyecto

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'titular', 'inversion')
    list_filter = ('nombre', 'titular', 'inversion', 'ingreso')
    search_fields = ('nombre', 'tipo', 'region', 'tipologia', 'inversion', 'ingreso')
    ordering = ('id',) 
