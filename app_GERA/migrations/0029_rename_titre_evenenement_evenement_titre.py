# Generated by Django 4.2.10 on 2024-04-26 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0028_rename_disponibilite_lieu_lieu_disponible'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evenement',
            old_name='Titre_Evenenement',
            new_name='Titre',
        ),
    ]
