# Generated by Django 4.2.10 on 2024-04-26 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0025_rename_description_organisateur_organisateur_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quartier',
            old_name='Ville',
            new_name='ID_Ville',
        ),
    ]
