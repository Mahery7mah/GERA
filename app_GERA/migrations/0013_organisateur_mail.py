# Generated by Django 4.2.10 on 2024-04-03 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0012_organisateur_description_organisateur'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisateur',
            name='Mail',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
