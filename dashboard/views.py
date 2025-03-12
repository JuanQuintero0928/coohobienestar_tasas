from django.shortcuts import render
from django.views.generic import ListView
from asociado.models import Asociado

# Create your views here.

class Dashboard(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'index.html'
        total = Asociado.objects.all().count()
        activo = Asociado.objects.filter(estadoAsociado = 'ACTIVO').count()
        retiro = Asociado.objects.filter(estadoAsociado = 'RETIRO').count()
        return render(request, template_name, {'total':total, 'activo':activo, 'retiro':retiro})
       
class Informacion(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/informacion.html'
        return render(request, template_name)