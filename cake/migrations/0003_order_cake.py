# Generated by Django 3.2.8 on 2021-10-28 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cake', '0002_auto_20211027_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cake',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='cake.cake', verbose_name='ัะพัั'),
        ),
    ]
