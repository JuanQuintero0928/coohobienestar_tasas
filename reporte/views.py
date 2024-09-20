from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.http import HttpResponse
from django.db.models.functions import TruncDate
from django.db.models import Sum
from datetime import timedelta

from asociado.models import Asociado, ParametroAsociado, TarifaAsociado
from historico.models import HistorialPagos
from parametro.models import MesTarifa
from funciones.function import fechaUtc, separarFecha

#Libreria para generar el Excel
from openpyxl import Workbook


class InformacionReporte(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'reporte/informacion.html'
        return render(request, template_name)

class VerPagosFecha(ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'reporte/pagosPorFecha.html'
        return render(request, template_name)
    
    def post(self, request, *args, **kwargs):
        fechaInicialForm = request.POST['fechaInicial']
        fechaFinalForm = request.POST['fechaFinal']
        # funcion que separa año, mes y dia de la fecha ingresada por el usuario.
        fechaInicial = separarFecha(fechaInicialForm, 'inicial')
        fechaFinal = separarFecha(fechaFinalForm, 'final')
        # consulta por rango de fecha inicial y final
        queryHistorial = HistorialPagos.objects.filter(
            fechaCreacion__range=[fechaInicial, fechaFinal]
        )
        template_name = 'reporte/pagosPorFecha.html'
        return render(request, template_name, {'query':queryHistorial,'post':'yes', 'fechaIncialF':fechaInicialForm, 'fechaFinalF':fechaFinalForm})

class ReporteExcelPago(TemplateView):
    def get(self, request, *args, **kwargs):
        fechaInicialForm = request.GET['fechaInicial']
        fechaFinalForm = request.GET['fechaFinal']
        # funcion que separa año, mes y dia de la fecha ingresada por el usuario.
        fechaInicial = separarFecha(fechaInicialForm, 'inicial')
        fechaFinal = separarFecha(fechaFinalForm, 'final')
        # consulta por rango de fecha inicial y final
        queryPagos = HistorialPagos.objects.filter(
            fechaCreacion__range=[fechaInicial, fechaFinal]
        )
        wb = Workbook() #Creamos la instancia del Workbook
        ws = wb.active
        ws.title = 'Pagos'
        titulo1 = f"Reporte de Pagos desde {fechaInicialForm} - {fechaFinalForm}"
        ws['A1'] = titulo1    #Casilla en la que queremos poner la informacion
        ws.merge_cells('A1:I1')

        ws['A2'] = 'Número Registro'
        ws['B2'] = 'Unidad de Servicio'
        ws['C2'] = 'Número Documento'
        ws['D2'] = 'Nombre Completo'
        ws['E2'] = 'Mes Pago'
        ws['F2'] = 'Valor Pago'
        ws['G2'] = 'Diferencia'
        ws['H2'] = 'Fecha Pago'
        ws['I2'] = 'Forma Pago'
     
        #Inicia el primer registro en la celda numero 3
        cont = 3
        i = 1
        for pago in queryPagos:
            #Row, son las filas , A,B,C,D osea row es igual al contador, y columnas 1,2,3
            ws.cell(row = cont, column = 1).value = i
            ws.cell(row = cont, column = 2).value = pago.asociado.hogarinfantil             
            ws.cell(row = cont, column = 3).value = int(pago.asociado.numDocumento)
            ws.cell(row = cont, column = 4).value = f'{pago.asociado.nombre}' + ' ' + f'{pago.asociado.apellido}'
            ws.cell(row = cont, column = 5).value = pago.mesPago.concepto
            ws.cell(row = cont, column = 6).value = pago.valorPago
            ws.cell(row = cont, column = 7).value = pago.diferencia
            ws.cell(row = cont, column = 8).value = pago.fechaPago
            ws.cell(row = cont, column = 9).value = pago.formaPago.formaPago
            i+=1
            cont+=1

        nombre_archivo = f"Reporte Pago_{fechaInicialForm}-{fechaFinalForm}.xlsx"
        response = HttpResponse(content_type = "application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response
    