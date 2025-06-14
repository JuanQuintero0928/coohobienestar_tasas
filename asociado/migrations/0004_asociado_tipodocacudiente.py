# Generated by Django 5.0.6 on 2025-06-09 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0003_asociado_nombreacudiente_asociado_numdocacudiente'),
    ]

    operations = [
        migrations.AddField(
            model_name='asociado',
            name='tipoDocAcudiente',
            field=models.CharField(blank=True, choices=[('CC', 'CEDULA'), ('RC', 'REGISTRO CIVIL'), ('TI', 'TARJETA IDENTIDAD'), ('CE', 'CEDULA EXTRANJERA'), ('PA', 'PASAPORTE'), ('PPT', 'PERMISO PROTECCION TEMPORAL'), ('SD', 'SIN DOCUMENTO')], default='CC', null=True, verbose_name='Tipo Documento Acudiente'),
        ),
    ]
