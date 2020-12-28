# Generated by Django 3.0.7 on 2020-12-21 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0035_auto_20200928_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=50, verbose_name='Имя клиента')),
                ('customer_lastname', models.CharField(max_length=50, verbose_name='Фамилия клиента')),
                ('customer_phonenumber', models.CharField(max_length=25, verbose_name='Номер телефона клиента')),
                ('customer_address', models.CharField(max_length=500, verbose_name='Адрес клиента')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
    ]