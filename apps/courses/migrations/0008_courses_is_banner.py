# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-12 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20170407_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u8f6e\u64ad'),
        ),
    ]
