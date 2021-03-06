# Generated by Django 2.2.24 on 2021-10-25 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20211025_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Windows',
            fields=[
                ('id_window', models.IntegerField(primary_key=True, serialize=False)),
                ('accept', models.BooleanField(default=True)),
                ('receive', models.BooleanField(default=True)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Users')),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id_ticket', models.IntegerField(primary_key=True, serialize=False)),
                ('name_ticket', models.CharField(max_length=50)),
                ('time_create', models.DateField()),
                ('time_close', models.DateField()),
                ('id_window', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Windows')),
            ],
        ),
    ]
