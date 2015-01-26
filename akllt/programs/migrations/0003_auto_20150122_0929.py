# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0002_auto_20150122_0924'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryPageRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('category', modelcluster.fields.ParentalKey(to='programs.CategoryPage')),
                ('program', modelcluster.fields.ParentalKey(to='programs.ProgramPage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
