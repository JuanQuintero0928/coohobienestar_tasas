from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('informacionReporte/', login_required(InformacionReporte.as_view()), name='informacionReporte'),
    path('verPagosPorFecha/', login_required(VerPagosFecha.as_view()), name='verPagosPorFecha'),
    path('generarPagoExcel/', login_required(ReporteExcelPago.as_view()), name='generarPagoExcel'),   
]