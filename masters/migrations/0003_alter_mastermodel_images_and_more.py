# Generated by Django 4.1.1 on 2022-10-06 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0002_mastermodel_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mastermodel',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='images', to='masters.masterimagesmodel', verbose_name='images'),
        ),
        migrations.AlterField(
            model_name='mastermodel',
            name='profession',
            field=models.ManyToManyField(blank=True, related_name='profession', to='masters.masterprofessionmodel', verbose_name='profession'),
        ),
    ]
