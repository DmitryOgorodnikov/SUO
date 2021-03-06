# Generated by Django 2.2.24 on 2022-04-14 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_auto_20211127_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='service_p',
            field=models.CharField(max_length=50, null=True, verbose_name='Услуга'),
        ),
        migrations.AddField(
            model_name='tickets',
            name='status',
            field=models.CharField(max_length=50, null=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='logwindows',
            name='id_window',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.Windows', verbose_name='ID Окна'),
        ),
        migrations.AlterField(
            model_name='logwindows',
            name='operator',
            field=models.CharField(max_length=50, null=True, verbose_name='Оператор'),
        ),
        migrations.AlterField(
            model_name='logwindows',
            name='time_login',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время входа'),
        ),
        migrations.AlterField(
            model_name='logwindows',
            name='time_logout',
            field=models.DateTimeField(null=True, verbose_name='Время выхода'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='chief',
            field=models.BooleanField(default=False, verbose_name='Начальник'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='windows',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Окно активно'),
        ),
        migrations.AlterField(
            model_name='windows',
            name='banking',
            field=models.BooleanField(default=True, verbose_name='Банковские услуги'),
        ),
        migrations.AlterField(
            model_name='windows',
            name='business',
            field=models.BooleanField(default=True, verbose_name='Услуги для бизнеса'),
        ),
        migrations.AlterField(
            model_name='windows',
            name='finance',
            field=models.BooleanField(default=True, verbose_name='Финансовые услуги'),
        ),
        migrations.AlterField(
            model_name='windows',
            name='other',
            field=models.BooleanField(default=True, verbose_name='Прочее'),
        ),
        migrations.AlterField(
            model_name='windows',
            name='purchase',
            field=models.BooleanField(default=True, verbose_name='Покупка товара'),
        ),
        migrations.AlterField(
            model_name='windows',
            name='receiving',
            field=models.BooleanField(default=True, verbose_name='Получение'),
        ),
        migrations.AlterField(
            model_name='windows',
            name='sending',
            field=models.BooleanField(default=True, verbose_name='Отправка'),
        ),
    ]
