# Generated by Django 3.1.4 on 2021-01-22 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0043_auto_20210122_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='choices',
            field=models.CharField(choices=[('cash', 'Наличные'), ('card', 'Картой')], default='cash', max_length=11, verbose_name='Способ оплаты'),
        ),
    ]
