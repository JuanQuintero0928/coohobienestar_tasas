from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, F, Q, Subquery

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

# No se usa 
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


class ModalPago(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/modalPago.html'
        queryValor = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        queryParamAsoc = ParametroAsociado.objects.get(asociado = kwargs['pkAsociado'])
        queryHistorial = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).exists()


        
       
        if queryHistorial:
            mesesPagados = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).values('mesPago')
            queryMes = (MesTarifa.objects
                        .exclude(pk__in=Subquery(mesesPagados))
                        .filter(pk__gte = queryParamAsoc.primerMes.pk))
        else:
            queryMes = MesTarifa.objects.filter(pk__gte = queryParamAsoc.primerMes.pk)
        
        queryPago = FormaPago.objects.all()

        queryHistorial = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado']).aggregate(total=Sum('diferencia'))
        total_diferencia = queryHistorial['total'] or 0  # Se obtiene el valor de la suma a 0 si no hay datos
        return render(request, template_name, {'pkAsociado':kwargs['pkAsociado'], 'vista':kwargs['vista'] ,'query':queryValor, 'queryMes':queryMes, 'queryPago':queryPago, 'diferencia':total_diferencia})

    def post(self, request, *args, **kwargs):
        fechaPago = request.POST['fechaPago']
        formaPago = request.POST['formaPago']
        valorPago = int(request.POST['valorPago'])
        tarifaAsociado = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        diferencia = request.POST['diferencia']
        valorDiferencia = int(diferencia.replace('.', ''))

        # creamos un array para guardar los pagos que se marcaron como activos
        datos_pagos = []

        # obtenemos los switchs que se marcaron como activos en el modal
        switches_activos = request.POST.getlist('switches')
        # saber el tamaño de los botones marcados
        cantidadSwitches = len(switches_activos)
        
        # Se recorre los switch activos, con el pk del mes activo
        for contador, pk in enumerate(switches_activos, start=1):
            valorMes = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado']).cuota
            pago = {
                    'asociado': Asociado.objects.get(pk = kwargs['pkAsociado']),
                    'mesPago': MesTarifa.objects.get(pk = pk),
                    'fechaPago': fechaPago,
                    'formaPago': FormaPago.objects.get(pk = formaPago),
                    'diferencia': valorDiferencia if cantidadSwitches == contador else 0,
                    'valorPago':  valorMes if contador < cantidadSwitches else valorMes + valorDiferencia,
                    'estadoRegistro': True,
                    'userCreacion': User.objects.get(pk = request.user.pk),
                }
            datos_pagos.append(pago)

        # Crear cada registro en un bucle
        for data in datos_pagos:
            HistorialPagos.objects.create(**data)
        
        messages.info(request, 'Pago Registrado Correctamente')
        url = reverse('proceso:asociadoPago')

        # Ajusta la URL según el valor de vista
        if kwargs['vista'] == 1:
            url = reverse('asociado:historialPagos', args=[kwargs['pkAsociado']])

        return HttpResponseRedirect(url)

class EditarPago(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'proceso/pago/editarPagoAsociado.html'
        queryPago = HistorialPagos.objects.get(pk = kwargs['pk'])
        queryMes = MesTarifa.objects.all()
        queryFormaPago = FormaPago.objects.all()
        return render(request, template_name, {'queryPago':queryPago, 'queryFormaPago':queryFormaPago, 'queryMes':queryMes, 'pk':kwargs['pk'], 'pkAsociado':kwargs['pkAsociado'], 'vista':kwargs['vista']})
    
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
        url = reverse('proceso:historicoPagos')

        # Ajusta la URL según el valor de vista
        if kwargs['vista'] == 1:
            url = reverse('asociado:historialPagos', args=[kwargs['pkAsociado']])

        return HttpResponseRedirect(url)
