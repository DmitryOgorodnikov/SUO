# Generated by Django 2.2.24 on 2021-11-27 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='windows',
            old_name='accept',
            new_name='receiving',
        ),
        migrations.RenameField(
            model_name='windows',
            old_name='receive',
            new_name='sending',
        ),
    ]
