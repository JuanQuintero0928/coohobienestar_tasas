from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('asociado/', login_required(Asociados.as_view()), name='asociado'),
    path('crearAsociado/', login_required(CrearAsociado.as_view()), name='crearAsociado'),
    path('editarAsociado/<int:pkAsociado>', login_required(EditarAsociado.as_view()), name='editarAsociado'),
    path('verAsociado/<int:pkAsociado>', login_required(VerAsociado.as_view()), name='verAsociado'),
    path('historialPagos/<int:pkAsociado>', login_required(VerHistorialPagos.as_view()), name='historialPagos'),
    path('detallePago/<int:pkAsociado>/<int:pk>', login_required(DetalleHistorialPago.as_view()), name='detallePago'),
    path('editarParametroAsociado/<int:pkAsociado>', login_required(EditarParametroAsociado.as_view()), name='editarParametroAsociado'),
]