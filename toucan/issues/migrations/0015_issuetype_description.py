# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-08 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0014_remove_issue_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuetype',
            name='description',
            field=models.TextField(blank=True, verbose_name='a short description of the issue type'),
        ),
    ]
