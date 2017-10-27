# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-24 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eis', '0032_auto_20171025_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emp_event_organized',
            name='role',
            field=models.CharField(choices=[('Convener', 'Convener'), ('Coordinator', 'Coordinator'), ('Co-Convener', 'Co-Convener')], max_length=11),
        ),
        migrations.AlterField(
            model_name='emp_event_organized',
            name='type',
            field=models.CharField(choices=[('Training Program', 'Training Program'), ('Seminar', 'Seminar'), ('Short Term Program', 'Short Term Program'), ('Workshop', 'Workshop'), ('Any Other', 'Any Other')], max_length=18),
        ),
    ]
