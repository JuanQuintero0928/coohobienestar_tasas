from django.db import models
from departamento.models import Departamento, Municipio
from parametro.models import MesTarifa
# from historico.models import TarifaAsociado

# Create your models here.

class Asociado(models.Model):

    class tipoDocumentoOp(models.TextChoices):
        cc = 'CC', 'CEDULA' 
        rc = 'RC', 'REGISTRO CIVIL'
        ti = 'TI', 'TARJETA IDENTIDAD'
        ce = 'CE', 'CEDULA EXTRANJERA'
        pa = 'PA', 'PASAPORTE'
        ppt = 'PPT', 'PERMISO PROTECCION TEMPORAL'
        sd = 'SD', 'SIN DOCUMENTO'

    class estadoAsociadoOp(models.TextChoices):
        activo = 'ACTIVO', 'ACTIVO'
        # inactivo = 'INACTIVO', 'INACTIVO'
        retirado = 'RETIRO', 'RETIRO'

    class hogarInfantilOp(models.TextChoices):
        sardinitos = 'SARDINITOS', 'SARDINITOS'
        jesusobrero = 'JESUS OBRERO', 'JESUS OBRERO'

    id = models.AutoField(primary_key=True)
    nombre1 = models.CharField('Primer Nombre', max_length=30, null=True, blank=True)
    nombre2 = models.CharField('Segundo Nombre', max_length=30, null=True, blank=True)
    apellido1 = models.CharField('Primer Apellido', max_length=30, null=True, blank=True)
    apellido2 = models.CharField('Segundo Apellido', max_length=30, null=True, blank=True)
    tipoDocumento = models.CharField('Tipo Documento', choices=tipoDocumentoOp.choices, default=tipoDocumentoOp.rc, blank=False, null=False)
    numDocumento = models.CharField('Número Documento', max_length=12, blank=False, null=False)
    numCelular = models.CharField('Numero Celular', max_length=11, blank=False, null=False)
    hogarinfantil = models.CharField('HogarInfantil', choices=hogarInfantilOp.choices, default=hogarInfantilOp.sardinitos, blank=False, null=False)
    estadoAsociado = models.CharField('Estado Asociado', choices=estadoAsociadoOp.choices, default=estadoAsociadoOp.activo, blank=False, null=False)
    desplazado = models.BooleanField('Desplazado', default=False, blank=False, null=False)
    nombreAcudiente = models.CharField('Nombre Acudiente', max_length=50, null=True, blank=True)
    numDocAcudiente = models.CharField('Número Documento Acudiente', max_length=12, null=True, blank=True)
    tipoDocAcudiente = models.CharField('Tipo Documento Acudiente', choices=tipoDocumentoOp.choices, default=tipoDocumentoOp.cc, blank=True, null=True)
    direccion = models.CharField('Dirección', blank=True, null=True)
    ciudadResidencia = models.CharField('Ciudad', blank=True, null=True)
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
    
