# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-24 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eis', '0029_auto_20171024_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emp_research_projects',
            name='status',
            field=models.CharField(choices=[('Awarded', 'Awarded'), ('Submitted', 'Submitted'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed')], max_length=10),
        ),
    ]
