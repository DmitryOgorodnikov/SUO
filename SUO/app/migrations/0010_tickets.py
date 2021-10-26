# Generated by Django 2.2.24 on 2021-10-25 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_windows'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id_ticket', models.IntegerField(primary_key=True, serialize=False)),
                ('name_ticket', models.CharField(max_length=50)),
                ('time_create', models.DateField()),
                ('time_close', models.DateField()),
            ],
        ),
    ]