# Generated by Django 4.1.5 on 2023-03-16 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0032_remove_mastermodel_youtube_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mastermodel',
            name='phone',
            field=models.IntegerField(default=0, verbose_name='phone'),
        ),
    ]
