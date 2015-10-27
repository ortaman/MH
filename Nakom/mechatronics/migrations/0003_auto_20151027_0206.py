# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mechatronics', '0002_auto_20151027_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('servicio', models.CharField(help_text=b'Servicio mensual', max_length=11)),
                ('monto', models.FloatField(help_text=b'Monto pagado mensual')),
                ('fecha_de_pago', models.DateField(default=datetime.datetime.now, help_text=b'Fecha de Pago')),
            ],
        ),
        migrations.AlterField(
            model_name='cliente',
            name='rfc',
            field=models.CharField(max_length=13, null=True, verbose_name=b'RFC', blank=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='empleado',
            field=models.ForeignKey(verbose_name=b'Asignaci\xc3\xb3n', to='mechatronics.Empleado', help_text=b'Empleado asignado al equipo'),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='entrega',
            field=models.DateField(help_text=b'Fecha tentativa de entrega'),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='registro',
            field=models.ForeignKey(verbose_name=b'Registr\xc3\xb3', to=settings.AUTH_USER_MODEL, help_text=b'Usuario que registr\xc3\xb3 el equipo'),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='total',
            field=models.FloatField(default=0.0, verbose_name=b'Costo total'),
        ),
    ]
