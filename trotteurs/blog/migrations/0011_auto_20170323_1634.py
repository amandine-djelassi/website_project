# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20170323_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag'),
        ),
    ]
