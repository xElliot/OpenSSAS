# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-25 10:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('injection_test', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='target',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targets', to='injection_test.Task'),
        ),
    ]
