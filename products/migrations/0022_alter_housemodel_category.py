# Generated by Django 4.1.1 on 2022-10-09 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_alter_housemodel_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housemodel',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='products.categorymodel', verbose_name='category'),
        ),
    ]
