# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('akllt', '0002_newsstory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsstory',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
