# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-07 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eis', '0006_auto_20171007_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emp_research_papers',
            name='is_sci',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=1, null=True),
        ),
    ]
