# Generated by Django 4.1.1 on 2022-10-08 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_remove_mastermodel_activity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housemodel',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='products.categorymodel', verbose_name='category'),
        ),
    ]
