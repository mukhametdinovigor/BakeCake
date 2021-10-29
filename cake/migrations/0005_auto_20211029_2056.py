# Generated by Django 3.2.8 on 2021-10-29 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cake', '0004_auto_20211029_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='доставлен в'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.DateTimeField(db_index=True, verbose_name='дата и время доставки'),
        ),
    ]