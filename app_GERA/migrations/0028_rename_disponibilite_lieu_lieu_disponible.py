# Generated by Django 4.2.10 on 2024-04-26 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0027_rename_quartier_adresse_id_quartier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lieu',
            old_name='Disponibilite_Lieu',
            new_name='Disponible',
        ),
    ]
