# Generated by Django 5.0.6 on 2025-03-12 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asociado',
            name='numDocumento',
            field=models.CharField(max_length=12, verbose_name='Número Documento'),
        ),
    ]
