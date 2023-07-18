# Generated by Django 4.1.5 on 2023-07-18 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_customuser_referrer_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='invited_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
