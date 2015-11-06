# encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from datetime import datetime


class Cliente(models.Model):
    nombre = models.CharField(max_length=22)
    apellido = models.CharField(max_length=22)

    telefono = models.CharField(max_length=22)
    email = models.EmailField(max_length=22, default='user@example.com',
                              verbose_name='e-mail')
    direccion = models.CharField(max_length=50, blank=True, null=True,
                                 verbose_name='dirección')

    rfc = models.CharField(max_length=13, blank=True,
                           null=True, verbose_name='RFC')
    razon_social = models.CharField(max_length=44, blank=True, null=True)

    registro = models.DateField(auto_now=True, help_text='Fecha de registro')

    class Meta:
        unique_together = ('nombre', 'apellido', )

    def __unicode__(self):
        return '%s %s' % (self.nombre, self.apellido, )


class Empleado(models.Model):
    CHOICES_ESTADO = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )

    nombre = models.CharField(max_length=22)
    apellido = models.CharField(max_length=22)

    telefono = models.CharField(max_length=22)
    email = models.EmailField(max_length=22, default='user@example.com',
                              verbose_name='e­-mail')

    direccion = models.CharField(max_length=44)

    registro = models.DateField(auto_now=True, help_text='Fecha de registro')

    estado = models.CharField(
        max_length=8,
        choices=CHOICES_ESTADO,
        default='activo',
        help_text='Estado del Empleado'
    )

    salario_base = models.FloatField(help_text='Salario semanal')
    comision = models.FloatField(help_text='Porcentaje')

    class Meta:
        unique_together = ('nombre', 'apellido',)

    def __unicode__(self):
        return '%s %s' % (self.nombre, self.apellido, )


class Servicio(models.Model):
    servicio = models.TextField(help_text='Descripción del servicio')
    costo = models.FloatField(help_text='Costo del servicio')

    def __unicode__(self):
        return self.servicio


class Equipo(models.Model):
    CHOICES_ESTATUS = (
        ('almacenado', 'Almacenado'),
        ('diagnosticado', 'Diagnosticado'),
        ('reparado', 'Reparado'),
        ('entregado', 'Entregado'),
        ('irreparable', 'Irreparable'),
    )
    folio = models.CharField(max_length=6, unique=True, help_text='Número de Folio')

    tipo = models.CharField(max_length=22, help_text='Información del equipo')
    marca = models.CharField(max_length=22, help_text='Marca del equipo')
    modelo = models.CharField(max_length=22, help_text='Modelo del equipo')

    ingreso = models.DateField(auto_now=True,
                               help_text='Fecha de ingreso del equipo')
    entrega = models.DateField(help_text='Fecha tentativa de entrega')
    estatus = models.CharField(max_length=13, default='almacenado',
                               choices=CHOICES_ESTATUS)

    servicios = models.ManyToManyField(Servicio,
                                       help_text='Servicios aplicados')

    total = models.FloatField(default=0.0, verbose_name='Costo total')

    cliente = models.ForeignKey(Cliente,
                                help_text='Propietario del equipo')
    empleado = models.ForeignKey(Empleado, verbose_name='Asignación',
                                 help_text='Empleado asignado al equipo')
    registro = models.ForeignKey(User, verbose_name='Registró',
                                 help_text='Usuario que registró el equipo')

    def __unicode__(self):
        return '%s %s' % (self.tipo, self.marca)


class Pago(models.Model):
    servicio = models.CharField(max_length=11, help_text='Servicio mensual')
    monto = models.FloatField(help_text='Monto pagado mensual')
    fecha_de_pago = models.DateField(default=datetime.now,
                                     help_text='Fecha de Pago')

    def __unicode__(self):
        return self.servicio
