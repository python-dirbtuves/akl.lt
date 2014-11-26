# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.tags
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('news', '0002_newsindex'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('content_object', modelcluster.fields.ParentalKey(to='news.NewsStory', related_name='news')),
                ('tag', models.ForeignKey(to='taggit.Tag', related_name='news_blogpagetag_items')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='newsstory',
            name='tags',
            field=modelcluster.tags.ClusterTaggableManager(to='taggit.Tag', through='news.BlogPageTag', help_text='A comma-separated list of tags.', blank=True, verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
