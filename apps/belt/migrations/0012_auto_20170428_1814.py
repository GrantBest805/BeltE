# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-28 18:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belt', '0011_auto_20170428_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='belt.User'),
        ),
    ]