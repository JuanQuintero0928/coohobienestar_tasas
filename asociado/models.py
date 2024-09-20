from django.db import models
from departamento.models import Departamento, Municipio
from parametro.models import MesTarifa
# from historico.models import TarifaAsociado

# Create your models here.

class Asociado(models.Model):

    class tipoDocumentoOp(models.TextChoices):
        cedula = 'CEDULA', 'CEDULA' 
        registroCivil = 'REGISTRO CIVIL', 'REGISTRO CIVIL'
        tarjetaIdentidad = 'TARJETA IDENTIDAD', 'TARJETA IDENTIDAD'
        cedulaExtranjera = 'CEDULA EXTRANJERA', 'CEDULA EXTRANJERA'
        pasaporte = 'PASAPORTE', 'PASAPORTE'

    class estadoAsociadoOp(models.TextChoices):
        activo = 'ACTIVO', 'ACTIVO'
        # inactivo = 'INACTIVO', 'INACTIVO'
        retirado = 'RETIRO', 'RETIRO'

    class hogarInfantilOp(models.TextChoices):
        angelitos = 'ANGELITOS', 'ANGELITOS'
        celmira = 'CELMIRA MEJIA', 'CELMIRA MEJIA'
        isabela = 'ISABELA', 'ISABELA'
        niñoPraga = 'NIÑO DE PRAGA', 'NIÑO DE PRAGA'
        santander = 'SANTANDER', 'SANTANDER'

    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre', max_length=30, null=False, blank=False)
    apellido = models.CharField('Apellido', max_length=30, null=False, blank=False)
    tipoDocumento = models.CharField('Tipo Documento', choices=tipoDocumentoOp.choices, default=tipoDocumentoOp.cedula, blank=False, null=False)
    numDocumento = models.CharField('Número Documento', max_length=10, blank=False, null=False)
    numCelular = models.CharField('Numero Celular', max_length=11, blank=False, null=False)
    hogarinfantil = models.CharField('HogarInfantil', choices=hogarInfantilOp.choices, default=hogarInfantilOp.angelitos, blank=False, null=False)
    estadoAsociado = models.CharField('Estado Asociado', choices=estadoAsociadoOp.choices, default=estadoAsociadoOp.activo, blank=False, null=False)
    estadoRegistro = models.BooleanField('Estado')
    fechaIngreso = models.DateField('Fecha Ingreso', blank=True, null=True)
    fechaRetiro = models.DateField('Fecha Retiro', blank=True, null=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = 'Asociado'
        ordering = ['pk']
    
    def __str__(self):
        return f"{self.id}"

class TarifaAsociado(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    cuota = models.IntegerField('Aporte', blank=False, null=False)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tarifa Por Asociado'
        verbose_name_plural = 'Tarifa Por Asociado'
        ordering = ['pk']
    
    def __str__(self):
        return f"{self.id}"

class ParametroAsociado(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    primerMes = models.ForeignKey(MesTarifa, on_delete=models.RESTRICT, blank=True, null=True)
    tarifaAsociado = models.ForeignKey(TarifaAsociado, on_delete=models.RESTRICT, blank=True, null=True)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Parametros Asociado'
        ordering = ['pk']
    
    def __str__(self):
        return  f"{self.asociado}"
    