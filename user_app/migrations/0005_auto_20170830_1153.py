# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 11:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0004_extrainfo_about_me'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrainfo',
            name='about_me',
            field=models.TextField(default='', max_length=1000),
        ),
    ]