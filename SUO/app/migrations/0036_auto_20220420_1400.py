# Generated by Django 2.2.24 on 2022-04-20 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_auto_20220414_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='windows',
            name='banking',
        ),
        migrations.RemoveField(
            model_name='windows',
            name='business',
        ),
        migrations.RemoveField(
            model_name='windows',
            name='finance',
        ),
        migrations.RemoveField(
            model_name='windows',
            name='other',
        ),
        migrations.RemoveField(
            model_name='windows',
            name='purchase',
        ),
        migrations.RemoveField(
            model_name='windows',
            name='receiving',
        ),
        migrations.RemoveField(
            model_name='windows',
            name='sending',
        ),
    ]
