# Generated by Django 4.1.5 on 2023-04-11 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0113_housemodel_descriptions_ru_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housemodel',
            name='youtube_link',
            field=models.FileField(blank=True, null=True, upload_to='Videos', verbose_name='youtube_link'),
        ),
    ]