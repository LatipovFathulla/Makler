# Generated by Django 4.1.5 on 2023-03-19 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mebel', '0012_mebelmodel_product_status_mebelmodel_view_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='mebelmodel',
            name='isBookmarked',
            field=models.BooleanField(default=False, verbose_name='isBookmarked'),
        ),
    ]
