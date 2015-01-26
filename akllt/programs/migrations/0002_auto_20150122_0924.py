# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryprogramrelation',
            name='category',
        ),
        migrations.RemoveField(
            model_name='categoryprogramrelation',
            name='program',
        ),
        migrations.DeleteModel(
            name='CategoryProgramRelation',
        ),
        migrations.AddField(
            model_name='programpage',
            name='categories',
            field=models.ManyToManyField(to='programs.CategoryPage'),
            preserve_default=True,
        ),
    ]
