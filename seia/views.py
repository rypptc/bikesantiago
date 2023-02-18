from django.shortcuts import render
from seia.models import Proyecto


def seia(request):
    proyectos = Proyecto.objects.all()
    context = {'proyectos': proyectos}
    return render(request, 'seia.html', context)
