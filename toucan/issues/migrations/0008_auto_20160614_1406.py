# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-14 14:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0007_auto_20160614_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='issue_type',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='issues.IssueType', verbose_name='issue type'),
        ),
    ]