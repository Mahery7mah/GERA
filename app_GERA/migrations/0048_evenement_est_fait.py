# Generated by Django 5.0.6 on 2024-05-26 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0047_rename_date_e_evenement_date_debut_e_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evenement',
            name='Est_Fait',
            field=models.BooleanField(null=True),
        ),
    ]
