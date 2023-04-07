# Generated by Django 4.1.5 on 2023-04-07 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carousel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='carouselmodel',
            name='image',
            field=models.FileField(null=True, upload_to='carousel/images', verbose_name='image'),
        ),
    ]
