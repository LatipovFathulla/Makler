# Generated by Django 4.1.5 on 2023-09-13 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mebel', '0017_mebelcategorymodel_title_ru_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mebelmodel',
            name='web_address_title_ru',
        ),
        migrations.RemoveField(
            model_name='mebelmodel',
            name='web_address_title_uz',
        ),
    ]