# Generated by Django 4.2.10 on 2024-04-03 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0011_evenement_date_arrive'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisateur',
            name='Description_organisateur',
            field=models.CharField(default='', max_length=255),
        ),
    ]