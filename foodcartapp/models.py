from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField('название', max_length=50)
    address = models.CharField('адрес', max_length=100, blank=True)
    contact_phone = models.CharField(
        'контактный телефон', max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'


class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.distinct().filter(menu_items__availability=True)


class ProductCategory(models.Model):
    name = models.CharField('название', max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('название', max_length=50)
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='категория', related_name='products')
    price = models.DecimalField('цена', max_digits=8, decimal_places=2)
    image = models.ImageField('картинка')
    special_status = models.BooleanField(
        'спец.предложение', default=False, db_index=True)
    description = models.TextField('описание', max_length=200, blank=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='menu_items')
    availability = models.BooleanField(
        'в продаже', default=True, db_index=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Необработанный'),
        ('cooking', 'Готовится'),
        ('delivery', 'На доставке'),
        ('done', 'Выполнен'),
        ('canceled', 'Отменен'),
    ]
    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Картой'),
    ]
    status = models.CharField(
        verbose_name='Статус заказа',
        max_length=11,
        choices=STATUS_CHOICES,
        default='new',
    )
    firstname = models.CharField(
        verbose_name='Имя клиента',
        max_length=50)
    lastname = models.CharField(
        verbose_name='Фамилия клиента',
        max_length=50)
    phonenumber = models.CharField(
        verbose_name='Номер телефона клиента',
        max_length=25)
    address = models.CharField(
        max_length=500,
        verbose_name='Адрес клиента',
    )
    comment = models.TextField('Комментарий',
                               blank=True)
    registered_at = models.DateTimeField('Время создания',
                                         default=timezone.now)
    called_at = models.DateTimeField('Время звонка',
                                     blank=True,
                                     null=True)
    delivered_at = models.DateTimeField('Время доставки',
                                        blank=True,
                                        null=True)
    max_length = 11,
    payment_type = models.CharField(
        verbose_name='Способ оплаты',
        max_length=11,
        choices=PAYMENT_CHOICES,
        default='cash',
    )

    def __str__(self):
        return f'{self.id}. {self.firstname} {self.lastname}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Товар'
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество',
        default=1)
    price = models.DecimalField(
        'Цена заказа', max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Содержимое заказа'
