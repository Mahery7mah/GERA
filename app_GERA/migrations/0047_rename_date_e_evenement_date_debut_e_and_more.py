# Generated by Django 4.2.10 on 2024-05-20 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0046_evenement_date_e'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evenement',
            old_name='Date_E',
            new_name='Date_Debut_E',
        ),
        migrations.RemoveField(
            model_name='evenement',
            name='Date_Heure_Debut_E',
        ),
        migrations.RemoveField(
            model_name='evenement',
            name='Date_Heure_Fin_E',
        ),
        migrations.AddField(
            model_name='evenement',
            name='Date_Fin_E',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='evenement',
            name='Heure_Debut_E',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='evenement',
            name='Heure_Fin_E',
            field=models.TimeField(null=True),
        ),
    ]
