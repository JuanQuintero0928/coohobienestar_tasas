from django.db import models

# Create your models here.
    
class Tarifas(models.Model):
    id = models.AutoField(primary_key=True)
    concepto = models.CharField('Concepto', max_length=30, null=False, blank=False)
    cuenta = models.IntegerField('Cuenta', null=False, blank=False)
    valor = models.IntegerField('Valor', null=False, blank=False)
    estadoRegistro = models.BooleanField('Estado')

    class Meta:
        verbose_name = 'Tarifa'
        verbose_name_plural = 'Tarifas'
        ordering = ['pk']
    
    def __str__(self):
        return self.concepto

class MesTarifa(models.Model):
    id = models.AutoField(primary_key=True)
    concepto = models.CharField('Concepto', max_length=30, null=False, blank=False)
    fechaInicio = models.DateField('Fecha Inicio', blank=True, null=True)
    fechaFinal = models.DateField('Fecha Final', blank=True, null=True)

    class Meta:
        verbose_name = 'Tarifa Por Mes'
        verbose_name_plural = 'Tarifa Por Mes'
        ordering = ['pk']
    
    def __str__(self):
        return self.concepto

class FormaPago(models.Model):
    id = models.AutoField(primary_key=True)
    formaPago = models.CharField('Forma Pago', max_length=30, null=False, blank=False)

    class Meta:
        verbose_name = 'Forma de Pago'
        verbose_name_plural = 'Forma de Pago'
        ordering = ['pk']
    
    def __str__(self):
        return self.formaPago