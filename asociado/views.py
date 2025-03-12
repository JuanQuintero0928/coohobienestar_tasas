from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F, Value
from django.db.models.functions import Concat, Coalesce
from django.urls import reverse_lazy

from .models import Asociado, ParametroAsociado, TarifaAsociado
from historico.models import HistorialPagos
from parametro.models import MesTarifa

# Create your views here.

class Asociados(ListView):
    template_name = 'base/asociado/listarAsociado.html'

    def get(self, request, *args, **kwargs):
        # Si es una petición AJAX, devolver JSON con paginación
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            start = int(request.GET.get('start', 0))
            length = int(request.GET.get('length', 10))
            search_value = request.GET.get('search_value', '').strip()  
            
            # Obtener columna y dirección de ordenación
            order_column_index = int(request.GET.get('order[0][column]', 0))
            order_direction = request.GET.get('order[0][dir]', 'asc')

            # Mapeo de columnas para ordenación
            column_map = [
                'id', 'nombre_completo', 'apellido_completo', 'numDocumento', 
                'hogarinfantil', 'numCelular', 'estadoAsociado'
            ]
            
            # Obtener columna de ordenación (por defecto 'id')
            order_column = column_map[order_column_index] if order_column_index < len(column_map) else 'id'
            
            # Aplicar orden ascendente o descendente
            if order_direction == 'desc':
                order_column = f'-{order_column}'

    
            query = Asociado.objects.values(
                        'id', 
                        'numDocumento', 
                        'hogarinfantil', 
                        'numCelular', 
                        'estadoAsociado'
                    ).annotate(
                        nombre_completo=Concat(F('nombre1'), Value(' '), Coalesce(F('nombre2'), Value(''))),
                        apellido_completo=Concat(F('apellido1'), Value(' '), Coalesce(F('apellido2'), Value('')))
                    ).order_by(order_column)


            # Aplicar filtro de búsqueda
            if search_value:
                query = query.filter(
                Q(nombre_completo__icontains=search_value) |
                Q(apellido_completo__icontains=search_value) |
                Q(numDocumento__icontains=search_value) |
                Q(hogarinfantil__icontains=search_value) |
                Q(numCelular__icontains=search_value) |
                Q(estadoAsociado__icontains=search_value)
            )

            total_records = query.count()

            # Aplicar paginación
            paginator = Paginator(query, length)
            page_number = (start // length) + 1
            page = paginator.get_page(page_number)

            return JsonResponse({
                'draw': int(request.GET.get('draw', 1)),
                'recordsTotal': total_records,
                'recordsFiltered': total_records,
                'data': list(page.object_list),
            }, safe=False)

        else:
            # Renderizar la plantilla en la primera carga
            return render(request, self.template_name)
    
class CrearAsociado(CreateView):
    template_name = 'base/asociado/crearAsociado.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'create':'yes'})
    
    def post(self, request, *args, **kwargs):
        
        numDoc = request.POST['numDocumento']
        validacion = Asociado.objects.filter(numDocumento = numDoc).exists()
        print(validacion)
        if validacion:
            messages.warning(request, 'El asociado con cedula '+ numDoc + ' ya existe en la base de datos.')
            return HttpResponseRedirect(reverse_lazy('asociado:asociado'))
        else:
            # se guarda informacion en el modelo ASOCIADO
            obj = Asociado()
            obj.hogarinfantil = request.POST['hogarinfantil']
            obj.nombre1 = request.POST['nombre1'].upper()
            if request.POST['nombre2'] != '':
                obj.nombre2 = request.POST['nombre2'].upper()
            obj.apellido1 = request.POST['apellido1'].upper()
            obj.apellido2 = request.POST['apellido2'].upper()
            obj.tipoDocumento = request.POST['tipoDocumento']
            obj.numDocumento = request.POST['numDocumento']
            obj.numCelular = request.POST['numCelular']
            obj.fechaIngreso = request.POST['fechaIngreso']
            obj.estadoAsociado = request.POST['estadoAsociado']
            obj.desplazado = 'desplazado' in request.POST
            obj.estadoRegistro = True
            obj.save()
            # se pone valor quemado en la busqueda con el pk, se busca tarifa de aportes y bienestar social
            objTarifaAsoc = TarifaAsociado()
            objTarifaAsoc.asociado = Asociado.objects.get(pk = obj.pk)
            objTarifaAsoc.cuota = request.POST['cuota']
            objTarifaAsoc.estadoRegistro = True
            objTarifaAsoc.save()
            # se guarda informacion en el modelo PARAMETROASOCIADO
            objParametro = ParametroAsociado()
            objParametro.asociado = Asociado.objects.get(pk = obj.pk)
            try:
                objParametro.primerMes = MesTarifa.objects.get(fechaInicio__lte = obj.fechaIngreso, fechaFinal__gte = obj.fechaIngreso)
            except Exception as e:
                objParametro.tarifaAsociado = TarifaAsociado.objects.get(pk = objTarifaAsoc.pk)
                objParametro.estadoRegistro = True
                objParametro.save()
                messages.info(request, 'Asociado Creado con hallazgo, fecha de inicio no se agrego en la bd.')
                return HttpResponseRedirect(reverse_lazy('asociado:verAsociado', args=[obj.pk]))
            objParametro.tarifaAsociado = TarifaAsociado.objects.get(pk = objTarifaAsoc.pk)
            objParametro.estadoRegistro = True
            objParametro.save()

            messages.info(request, 'Asociado Creado Correctamente')
            return HttpResponseRedirect(reverse_lazy('asociado:verAsociado', args=[obj.pk]))
            
        # except Exception as e:
        #     messages.error(request, 'Ocurrio un problema al crear el asociado, comuniquese con el administrador.')
        #     return HttpResponseRedirect(reverse_lazy('asociado:asociado'))
        
class VerAsociado(ListView):
    template_name = 'base/asociado/verAsociado.html'

    def get(self, request, *args, **kwargs):
        objAsociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        objTarifaAsociado = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        objParametroAsociado = ParametroAsociado.objects.get(asociado = kwargs['pkAsociado'])
        objMes = MesTarifa.objects.all()
        return render(request, self.template_name, {'pkAsociado':kwargs['pkAsociado'], 'objAsociado':objAsociado, 'objParametroAsociado':objParametroAsociado, 'objTarifaAsociado':objTarifaAsociado, 'objMes':objMes, 'vista':1})

class EditarAsociado(CreateView):
    template_name = 'base/asociado/editarAsociado.html'
        
    def post(self, request, *args, **kwargs):

        # se guarda informacion en el modelo ASOCIADO
        obj = Asociado.objects.get(pk = kwargs['pkAsociado'])
        # para retirar un asociado
        if request.POST['fechaRetiro'] != '' or request.POST['estadoAsociado'] == 'RETIRO':
            if request.POST['fechaRetiro'] == '':
                messages.warning(request, 'Debe llenar el campo Fecha Retiro')
                return HttpResponseRedirect(reverse_lazy('asociado:verAsociado', args=[kwargs['pkAsociado']]))
            if request.POST['estadoAsociado'] == 'ACTIVO':
                messages.warning(request, 'Debe confirmar el estado del asociado en "RETIRO"')
                return HttpResponseRedirect(reverse_lazy('asociado:verAsociado', args=[kwargs['pkAsociado']]))
            obj.fechaRetiro = request.POST['fechaRetiro']
            obj.estadoAsociado = 'RETIRO'
        obj.hogarinfantil = request.POST['hogarinfantil']
        obj.nombre1 = request.POST['nombre1'].upper()
        if request.POST['nombre2'] != '':
            obj.nombre2 = request.POST['nombre2'].upper()
        obj.apellido1 = request.POST['apellido1'].upper()
        obj.apellido2 = request.POST['apellido2'].upper()
        obj.tipoDocumento = request.POST['tipoDocumento']
        obj.numDocumento = request.POST['numDocumento']
        obj.numCelular = request.POST['numCelular']
        obj.fechaIngreso = request.POST['fechaIngreso']
        obj.estadoAsociado = 'ACTIVO'
        obj.fechaRetiro = None
        obj.estadoRegistro = True
        obj.save()
        # se pone valor quemado en la busqueda con el pk, se busca tarifa de aportes y bienestar social
        objTarifaAsoc = TarifaAsociado.objects.get(asociado = kwargs['pkAsociado'])
        objTarifaAsoc.asociado = Asociado.objects.get(pk = obj.pk)
        objTarifaAsoc.cuota = request.POST['cuota']
        objTarifaAsoc.estadoRegistro = True
        objTarifaAsoc.save()
        # se guarda informacion en el modelo PARAMETROASOCIADO
        objParametro = ParametroAsociado.objects.get(asociado = kwargs['pkAsociado'])
        objParametro.asociado = Asociado.objects.get(pk = obj.pk)
        objParametro.primerMes = MesTarifa.objects.get(fechaInicio__lte = obj.fechaIngreso, fechaFinal__gte = obj.fechaIngreso)
        objParametro.tarifaAsociado = TarifaAsociado.objects.get(pk = objTarifaAsoc.pk)
        objParametro.estadoRegistro = True
        objParametro.save()
        messages.info(request, 'Información Modificada Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:verAsociado', args=[kwargs['pkAsociado']]))
    
class VerHistorialPagos(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/historico/listarHistorialPago.html'
        queryPagos = HistorialPagos.objects.filter(asociado = kwargs['pkAsociado'])
        queryAsociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        return render(request, template_name, {'updateAsociado':'yes','pkAsociado':kwargs['pkAsociado'],'query':queryPagos, 'queryAsociado':queryAsociado, 'vista':9})
    
class DetalleHistorialPago(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'base/historico/detallePago.html'
        query = HistorialPagos.objects.get(pk = kwargs['pk'])
        return render(request, template_name, {'query':query})

class EditarParametroAsociado(CreateView):

    def post(self, request, *args, **kwargs):
        obj = ParametroAsociado.objects.get(asociado = kwargs['pkAsociado'])
        objAsociado = Asociado.objects.get(pk = kwargs['pkAsociado'])
        obj.primerMes = MesTarifa.objects.get(pk = request.POST['primesMes'])
        obj.save()
        objAsociado.save()
        messages.info(request, 'Información Modificada Correctamente')
        return HttpResponseRedirect(reverse_lazy('asociado:verAsociado', args=[kwargs['pkAsociado']]))

