# Generated by Django 4.1.5 on 2023-04-29 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_storemodel_brand_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='storebrandmodel',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='store-brand-image', verbose_name='image'),
        ),
    ]