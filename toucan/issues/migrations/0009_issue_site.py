# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-01 09:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('issues', '0008_auto_20160614_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
        ),
    ]
