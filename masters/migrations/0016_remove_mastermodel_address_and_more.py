# Generated by Django 4.1.1 on 2022-12-02 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0015_alter_mastermodel_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mastermodel',
            name='address',
        ),
        migrations.AddField(
            model_name='mastermodel',
            name='address_latitude',
            field=models.FloatField(max_length=90, null=True, verbose_name='address_latitude'),
        ),
        migrations.AddField(
            model_name='mastermodel',
            name='address_longitude',
            field=models.FloatField(max_length=90, null=True, verbose_name='address_longitude'),
        ),
        migrations.AddField(
            model_name='mastermodel',
            name='address_title',
            field=models.CharField(max_length=300, null=True, verbose_name='address_title'),
        ),
    ]
