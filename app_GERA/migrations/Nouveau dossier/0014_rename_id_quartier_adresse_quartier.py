# Generated by Django 4.2.10 on 2024-02-20 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0013_rename_id_adresse_lieu_adresse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adresse',
            old_name='ID_Quartier',
            new_name='Quartier',
        ),
    ]
