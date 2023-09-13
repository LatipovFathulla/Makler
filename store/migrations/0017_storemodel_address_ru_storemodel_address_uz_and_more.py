# Generated by Django 4.1.5 on 2023-09-13 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_howstoreservicemodel_title_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='storemodel',
            name='address_ru',
            field=models.CharField(max_length=400, null=True, verbose_name='address'),
        ),
        migrations.AddField(
            model_name='storemodel',
            name='address_uz',
            field=models.CharField(max_length=400, null=True, verbose_name='address'),
        ),
        migrations.AddField(
            model_name='storemodel',
            name='description_ru',
            field=models.TextField(null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='storemodel',
            name='description_uz',
            field=models.TextField(null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='storemodel',
            name='name_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='storemodel',
            name='name_uz',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
        ),
    ]
