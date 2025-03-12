# Generated by Django 5.0.6 on 2025-03-12 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormaPago',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('formaPago', models.CharField(max_length=30, verbose_name='Forma Pago')),
            ],
            options={
                'verbose_name': 'Forma de Pago',
                'verbose_name_plural': 'Forma de Pago',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='MesTarifa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('concepto', models.CharField(max_length=30, verbose_name='Concepto')),
                ('fechaInicio', models.DateField(blank=True, null=True, verbose_name='Fecha Inicio')),
                ('fechaFinal', models.DateField(blank=True, null=True, verbose_name='Fecha Final')),
            ],
            options={
                'verbose_name': 'Tarifa Por Mes',
                'verbose_name_plural': 'Tarifa Por Mes',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Tarifas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('concepto', models.CharField(max_length=30, verbose_name='Concepto')),
                ('cuenta', models.IntegerField(verbose_name='Cuenta')),
                ('valor', models.IntegerField(verbose_name='Valor')),
                ('estadoRegistro', models.BooleanField(verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Tarifa',
                'verbose_name_plural': 'Tarifas',
                'ordering': ['pk'],
            },
        ),
    ]
