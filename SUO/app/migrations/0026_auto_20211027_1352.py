# Generated by Django 2.2.24 on 2021-10-27 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_logwindows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='time_call',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='time_close',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]