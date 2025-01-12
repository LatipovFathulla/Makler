# Generated by Django 4.1.5 on 2023-04-07 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0112_alter_housemodel_app_ipoteka_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mebel', '0014_alter_mebelmodel_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mebelmodel',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mebel.mebelcategorymodel', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='mebelmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='mebelmodel',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mebels', to=settings.AUTH_USER_MODEL, verbose_name='creator'),
        ),
        migrations.AlterField(
            model_name='mebelmodel',
            name='draft',
            field=models.BooleanField(default=False, null=True, verbose_name='draft'),
        ),
        migrations.AlterField(
            model_name='mebelmodel',
            name='price_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='price_types_mebel', to='products.pricelistmodel', verbose_name='price_type'),
        ),
        migrations.AlterField(
            model_name='mebelmodel',
            name='product_status',
            field=models.IntegerField(choices=[(0, 'InProgress'), (1, 'PUBLISH'), (2, 'DELETED'), (3, 'ARCHIVED'), (4, 'REJECTED')], default=0, null=True, verbose_name='product status'),
        ),
        migrations.AlterField(
            model_name='mebelmodel',
            name='view_count',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='view_count'),
        ),
    ]
