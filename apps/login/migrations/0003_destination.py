# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-01 19:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20180301_1942'),
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('content', models.TextField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinations', to='login.User')),
                ('plans', models.ManyToManyField(related_name='plan', to='login.User')),
            ],
        ),
    ]
