# Generated by Django 4.1.5 on 2023-04-26 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0114_alter_housemodel_youtube_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymodel',
            name='subtitle_ru',
            field=models.TextField(null=True, verbose_name='subtitle'),
        ),
        migrations.AddField(
            model_name='categorymodel',
            name='subtitle_uz',
            field=models.TextField(null=True, verbose_name='subtitle'),
        ),
        migrations.AddField(
            model_name='categorymodel',
            name='title_ru',
            field=models.CharField(max_length=500, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='categorymodel',
            name='title_uz',
            field=models.CharField(max_length=500, null=True, verbose_name='title'),
        ),
    ]