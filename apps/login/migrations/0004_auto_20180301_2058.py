# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-01 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_destination'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='end_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='destination',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]