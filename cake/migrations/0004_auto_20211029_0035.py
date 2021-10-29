# Generated by Django 3.2.8 on 2021-10-28 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cake', '0003_order_cake'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_at',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='дата доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.TimeField(db_index=True, verbose_name='время доставки'),
        ),
    ]