# Generated by Django 3.1.4 on 2020-12-30 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0040_orderitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'Необработанный'), ('cooking', 'Готовится'), ('delivery', 'На доставке'), ('done', 'Выполнен'), ('canceled', 'Отменен')], default='new', max_length=11, verbose_name='Статус заказа'),
        ),
    ]