from django.shortcuts import render
from bikes_info.models import Station


def bikes(request):
    stations = Station.objects.all()
    context = {'stations': stations}
    return render(request, 'bikes.html', context)
