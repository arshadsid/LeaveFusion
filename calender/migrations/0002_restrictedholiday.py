# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-26 23:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calender', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestrictedHoliday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('date', models.DateField()),
            ],
        ),
    ]