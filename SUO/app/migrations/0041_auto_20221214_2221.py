# Generated by Django 2.2.24 on 2022-12-14 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_auto_20220426_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='time_create',
            field=models.DateTimeField(verbose_name='Время создания'),
        ),
    ]