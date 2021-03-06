# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-06 12:30
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.ranges
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisations', '0004_auto_20160614_1337'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToucanInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('invitation_valid_range', django.contrib.postgres.fields.ranges.DateTimeRangeField(editable=False)),
                ('invitation_sent', models.DateTimeField(null=True)),
                ('secret_key', models.CharField(editable=False, max_length=64, unique=True, validators=[django.core.validators.MinLengthValidator(64)])),
                ('role', models.IntegerField(choices=[(0, 'member'), (5, 'admin'), (10, 'owner')], default=0)),
                ('invited_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invited', to=settings.AUTH_USER_MODEL)),
                ('organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='organisations.Organisation')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invited_through', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
