# Generated by Django 4.2.10 on 2024-04-26 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0029_rename_titre_evenenement_evenement_titre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evenement',
            old_name='Description_Evenement',
            new_name='Description',
        ),
    ]
