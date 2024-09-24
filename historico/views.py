from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum

from .models import HistorialPagos
from parametro.models import MesTarifa, FormaPago
from asociado.models import Asociado, ParametroAsociado, TarifaAsociado

# Create your views here.

class VerHistoricoPagos(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/listarPagos.html'
        query = HistorialPagos.objects.all()
        return render(request, template_name, {'query':query})

class VerAsociadoPagos(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/realizarPago.html'
        query = TarifaAsociado.objects.select_related('asociado').all()
        return render(request, template_name, {'query':query})
    
class CrearPagoAsociado(CreateView):

    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/crearPagoAsociado.html'
        queryValor = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        queryParamAsoc = ParametroAsociado.objects.get(asociado = kwargs['pkAsociado'])
        queryHistorial = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).count()
        if queryHistorial == 0:
            queryMes = MesTarifa.objects.filter(pk__gte = queryParamAsoc.primerMes.pk)
        else:
            queryUltPago = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).last()
            queryMes = MesTarifa.objects.filter(pk__gt = queryUltPago.mesPago.pk)
        queryPago = FormaPago.objects.all()
        queryHistorial = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).aggregate(total=Sum('diferencia'))
        for valor in queryHistorial.values():
            diferencia = valor
        return render(request, template_name, {'pkAsociado':kwargs['pkAsociado'], 'query':queryValor, 'queryMes':queryMes, 'queryPago':queryPago, 'diferencia':diferencia})
   
    def post(self, request, *args, **kwargs):
        mesPago = int(request.POST['mesPago'])
        formaPago = int(request.POST['formaPago'])
        if mesPago == 0 or formaPago == 0:
            messages.warning(request, "Digite completamente el formulario, fecha y forma de pago.")
            return redirect('proceso:asociadoPago')
        else:
            valorPagoVerificacion = int(request.POST['valorPagoVerificacion'])
            valorPago = int(request.POST['valorPago'])
            obj = HistorialPagos()
            diferencia = 0
            # se valida si el valor pago es igual al valor real que debe pagar
            if valorPago != valorPagoVerificacion:
                diferencia = valorPago - valorPagoVerificacion

            obj.asociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
            obj.mesPago = MesTarifa.objects.get(pk = mesPago)
            obj.fechaPago = request.POST['fechaPago']
            obj.valorPago = valorPago
            obj.diferencia = diferencia
            obj.formaPago = FormaPago.objects.get(pk = formaPago)
            obj.estadoRegistro = True
            obj.userCreacion = User.objects.get(pk = request.user.pk)
            obj.save()
            messages.info(request, 'Pago Registrado Correctamente')
            return redirect('proceso:asociadoPago')

class EditarPago(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/editarPagoAsociado.html'
        queryPago = HistorialPagos.objects.get(pk = kwargs['pk'])
        queryMes = MesTarifa.objects.all()
        queryFormaPago = FormaPago.objects.all()
        return render(request, template_name, {'queryPago':queryPago, 'queryFormaPago':queryFormaPago, 'queryMes':queryMes, 'pk':kwargs['pk'], 'pkAsociado':kwargs['pkAsociado']})
    
    def post(self, request, *args, **kwargs):
        objHistorico = HistorialPagos.objects.get(pk = kwargs['pk'])
        objTarifa = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        valorPago = int(request.POST['valorPago'])
        # se valida si el valor pago es igual al valor real que debe pagar
        if valorPago != objTarifa.cuota:
            diferencia = valorPago - objTarifa.cuota
            objHistorico.diferencia = diferencia
        else:
            objHistorico.diferencia = 0
        objHistorico.mesPago = MesTarifa.objects.get(pk = request.POST['mesPago'])
        objHistorico.formaPago = FormaPago.objects.get(pk = request.POST['formaPago'])
        objHistorico.fechaPago = request.POST['fechaPago']
        objHistorico.valorPago = request.POST['valorPago']
        objHistorico.userModificacion = User.objects.get(pk = request.user.pk)
        objHistorico.save()
        messages.info(request, 'Pago Modificado Correctamente')
        return redirect('proceso:historicoPagos')
