# Generated by Django 2.2.24 on 2021-10-25 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='users',
            name='password',
            field=models.CharField(default='00000', max_length=50),
        ),
    ]
