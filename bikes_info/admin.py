from django.contrib import admin
from .models import Station

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('station_id', 'name', 'address')
    list_filter = ('name', 'payment')
    search_fields = ('name', 'address')
