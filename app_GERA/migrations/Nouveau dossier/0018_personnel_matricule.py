# Generated by Django 4.2.10 on 2024-03-16 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0017_remove_utilisateur_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnel',
            name='Matricule',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
    ]
