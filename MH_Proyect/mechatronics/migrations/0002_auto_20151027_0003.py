# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mechatronics', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicio',
            old_name='monto',
            new_name='costo',
        ),
        migrations.AlterField(
            model_name='servicio',
            name='servicio',
            field=models.TextField(help_text=b'Descripci\xc3\xb3n del servicio'),
        ),
    ]
