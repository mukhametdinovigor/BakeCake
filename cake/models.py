from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField


class Level(models.Model):
    levels_count = models.PositiveSmallIntegerField(
        'число уровней',
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
    )

    class Meta:
        verbose_name = 'число уровней'
        verbose_name_plural = 'числа уровней'

    def __str__(self):
        return f'{self.levels_count} уровней'


class Shape(models.Model):
    figure = models.CharField(
        'фигура',
        max_length=20,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
    )

    class Meta:
        verbose_name = 'форма'
        verbose_name_plural = 'формы'

    def __str__(self):
        return self.figure


class Topping(models.Model):
    name = models.CharField(
        'название',
        max_length=20,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
    )

    class Meta:
        verbose_name = 'топпинг'
        verbose_name_plural = 'топпинги'

    def __str__(self):
        return self.name


class Berry(models.Model):
    name = models.CharField(
        'название',
        max_length=20,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
    )

    class Meta:
        verbose_name = 'ягода'
        verbose_name_plural = 'ягоды'

    def __str__(self):
        return self.name


class AdditionalIngredient(models.Model):
    name = models.CharField(
        'название',
        max_length=20,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
    )

    class Meta:
        verbose_name = 'дополнительный ингредиент'
        verbose_name_plural = 'дополнительные ингредиенты'

    def __str__(self):
        return self.name


class Cake(models.Model):
    level = models.ForeignKey(
        Level,
        related_name='cakes',
        verbose_name='число уровней',
        on_delete=models.SET_NULL,
        null=True,
    )
    shape = models.ForeignKey(
        Shape,
        related_name='cakes',
        verbose_name='форма',
        on_delete=models.SET_NULL,
        null=True,
    )
    topping = models.ForeignKey(
        Topping,
        related_name='cakes',
        verbose_name='топпинг',
        on_delete=models.SET_NULL,
        null=True,
    )
    berries = models.ManyToManyField(
        Berry,
        related_name='cakes',
        verbose_name='ягоды',
        blank=True,
    )
    additional_ingredients = models.ManyToManyField(
        AdditionalIngredient,
        related_name='cakes',
        verbose_name='дополнительные ингредиенты',
        blank=True,
    )
    lettering = models.TextField(
        'подпись',
        null=True,
        blank=True,
        validators=[MaxLengthValidator(100)],
    )
    lettering_cost = models.FloatField(
        'цена подписи',
    )

    class Meta:
        verbose_name = 'торт'
        verbose_name_plural = 'торты'


class Customer(AbstractUser):
    phonenumber = PhoneNumberField(
        'номер телефона',
        max_length=20,
        validators=[MaxLengthValidator(12)],
    )
    address = models.CharField(
        'адрес',
        max_length=100,
    )
    social_network_link = models.TextField(
        'ссылка на соцсеть',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'покупатель'
        verbose_name_plural = 'покупатели'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Order(models.Model):
    STATUS = (
        ('PENDING', 'Заявка обрабатывается'),
        ('COOKED', 'Торт готовится'),
        ('EN_ROUTE', 'Торт в пути'),
        ('COMPLETED', 'Выполнен'),
        ('CANCELED', 'Отменен'),
    )

    status = models.CharField(
        'статус',
        max_length=20,
        choices=STATUS,
        default='PENDING',
        db_index=True,
    )
    created_at = models.DateTimeField(
        'создан в',
        default=timezone.now,
        db_index=True,
    )
    delivered_at = models.DateField(
        'дата доставки',
        blank=True,
        null=True,
        db_index=True,
    )
    delivery_time = models.TimeField(
        'время доставки',
        db_index=True,
    )

    comment = models.TextField(
        'комментарий к заказу',
        blank=True,
        null=True,
        validators=[MaxLengthValidator(300)],
    )
    total_price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
    )

    customer = models.ForeignKey(
        Customer,
        related_name='orders',
        verbose_name='покупатель',
        on_delete=models.CASCADE,
    )

    cake = models.ForeignKey(
        Cake,
        related_name='orders',
        verbose_name='торт',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ {self.customer.first_name} {self.customer.last_name} {self.created_at}'
