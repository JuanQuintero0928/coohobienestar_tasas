# Generated by Django 5.0.6 on 2024-09-20 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historico', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialpagos',
            name='fechaPago',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Pago'),
        ),
    ]
