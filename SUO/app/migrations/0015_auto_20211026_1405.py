# Generated by Django 2.2.24 on 2021-10-26 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20211026_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='windows',
            name='id_user',
            field=models.IntegerField(null=True),
        ),
    ]