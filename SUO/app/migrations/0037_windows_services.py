# Generated by Django 2.2.24 on 2022-04-20 11:04

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_auto_20220420_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='windows',
            name='services',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
