# Generated by Django 4.2.10 on 2024-04-03 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0010_remove_quartier_codepostal_ville_codepostal'),
    ]

    operations = [
        migrations.AddField(
            model_name='evenement',
            name='Date_arrive',
            field=models.DateField(null=True),
        ),
    ]
