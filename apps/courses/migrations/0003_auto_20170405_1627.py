# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-05 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_courses_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='category',
            field=models.CharField(default='\u540e\u7aef\u5f00\u53d1', max_length=50, verbose_name='\u8bfe\u7a0b\u540d'),
        ),
        migrations.AlterField(
            model_name='courses',
            name='degress',
            field=models.CharField(choices=[('cj', '\u521d\u7ea7'), ('zj', '\u4e2d\u7ea7'), ('gj', '\u9ad8\u7ea7')], max_length=2, verbose_name='\u8bfe\u7a0b\u96be\u5ea6'),
        ),
    ]
