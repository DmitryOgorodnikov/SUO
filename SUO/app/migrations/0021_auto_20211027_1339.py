# Generated by Django 2.2.24 on 2021-10-27 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20211027_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logwindows',
            name='time_login',
            field=models.TimeField(null=True),
        ),
    ]
