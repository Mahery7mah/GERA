# Generated by Django 4.2.10 on 2024-04-26 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0031_rename_adresse_lieu_id_adresse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membre',
            old_name='Poste',
            new_name='ID_Poste',
        ),
    ]
