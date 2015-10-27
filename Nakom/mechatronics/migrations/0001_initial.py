# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=22)),
                ('apellido', models.CharField(max_length=22)),
                ('telefono', models.CharField(max_length=22)),
                ('email', models.EmailField(default=b'user@example.com', max_length=22, verbose_name=b'e-mail')),
                ('direccion', models.CharField(max_length=50, null=True, verbose_name=b'direcci\xc3\xb3n', blank=True)),
                ('rfc', models.CharField(max_length=13, null=True, blank=True)),
                ('razon_social', models.CharField(max_length=44, null=True, blank=True)),
                ('registro', models.DateField(help_text=b'Fecha de registro', auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=22)),
                ('apellido', models.CharField(max_length=22)),
                ('telefono', models.CharField(max_length=22)),
                ('email', models.EmailField(default=b'user@example.com', max_length=22, verbose_name=b'e\xc2\xad-mail')),
                ('direccion', models.CharField(max_length=44)),
                ('registro', models.DateField(help_text=b'Fecha de registro', auto_now=True)),
                ('estado', models.CharField(default=b'activo', help_text=b'Estado del Empleado', max_length=8, choices=[(b'activo', b'Activo'), (b'inactivo', b'Inactivo')])),
                ('salario_base', models.FloatField(help_text=b'Salario semanal')),
                ('comision', models.FloatField(help_text=b'Porcentaje')),
            ],
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('folio', models.CharField(help_text=b'N\xc3\xbamero de Folio', max_length=6)),
                ('tipo', models.CharField(help_text=b'Informaci\xc3\xb3n del equipo', max_length=22)),
                ('marca', models.CharField(help_text=b'Marca del equipo', max_length=22)),
                ('modelo', models.CharField(help_text=b'Modelo del equipo', max_length=22)),
                ('ingreso', models.DateField(help_text=b'Fecha de ingreso del equipo', auto_now=True)),
                ('entrega', models.DateField(help_text=b'Fecha de entrega del equipo', null=True, blank=True)),
                ('estatus', models.CharField(default=b'almacenado', max_length=13, choices=[(b'almacenado', b'Almacenado'), (b'diagnosticado', b'Diagnosticado'), (b'reparado', b'Reparado'), (b'entregado', b'Entregado'), (b'inreparable', b'Irreparable')])),
                ('total', models.FloatField(default=0.0)),
                ('cliente', models.ForeignKey(help_text=b'Propietario del equipo', to='mechatronics.Cliente')),
                ('empleado', models.ForeignKey(help_text=b'Empleado asignado al equipo', to='mechatronics.Empleado')),
                ('registro', models.ForeignKey(help_text=b'Usuario que registr\xc3\xb3 el equipo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('servicio', models.CharField(help_text=b'Servicio mensual', max_length=25)),
                ('monto', models.FloatField(help_text=b'Costo del servicio')),
            ],
        ),
        migrations.AddField(
            model_name='equipo',
            name='servicios',
            field=models.ManyToManyField(help_text=b'Servicios aplicados', to='mechatronics.Servicio'),
        ),
        migrations.AlterUniqueTogether(
            name='empleado',
            unique_together=set([('nombre', 'apellido')]),
        ),
        migrations.AlterUniqueTogether(
            name='cliente',
            unique_together=set([('nombre', 'apellido')]),
        ),
    ]
