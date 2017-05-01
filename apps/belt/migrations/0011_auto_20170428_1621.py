# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-28 16:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belt', '0010_auto_20170428_0308'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='buddies',
            field=models.ManyToManyField(related_name='users_trips', to='belt.User'),
        ),
        migrations.RemoveField(
            model_name='trip',
            name='user_id',
        ),
        migrations.AddField(
            model_name='trip',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='belt.User'),
        ),
    ]
