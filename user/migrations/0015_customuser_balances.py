# Generated by Django 4.1.5 on 2023-07-17 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_customuser_invited_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='balances',
            field=models.IntegerField(default=0),
        ),
    ]