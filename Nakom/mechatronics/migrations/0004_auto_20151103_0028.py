# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mechatronics', '0003_auto_20151027_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='folio',
            field=models.CharField(help_text=b'N\xc3\xbamero de Folio', unique=True, max_length=6),
        ),
    ]
