from django.db import models
from asociado.models import Asociado
from parametro.models import MesTarifa, FormaPago

# Create your models here.

class HistorialPagos(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    mesPago = models.ForeignKey(MesTarifa, on_delete=models.RESTRICT, blank=False, null=False)
    fechaPago = models.DateField('Fecha Pago', blank=True, null=True)
    valorPago = models.IntegerField('Valor Pago', blank=False, null=False)
    diferencia = models.IntegerField('Diferencia', blank=True, null=True)
    formaPago = models.ForeignKey(FormaPago, on_delete=models.RESTRICT, blank=False, null=False)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Historial de Pagos'
        verbose_name_plural = 'Historial de Pagos'
        ordering = ['pk']
    
    def __str__(self):
        return f"{self.id}"
