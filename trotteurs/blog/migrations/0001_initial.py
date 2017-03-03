# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=200, verbose_name='Titre')),
                ('pub_date', models.DateTimeField(verbose_name='Date de publication')),
                ('abstract', models.CharField(max_length=200, verbose_name='Résumé')),
                ('text', models.TextField(verbose_name="Corps de l'article")),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('tag_titlle', models.CharField(max_length=200, verbose_name='Titre')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
