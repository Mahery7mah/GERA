# Generated by Django 4.2.10 on 2024-03-29 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0004_alter_utilisateur_options_alter_utilisateur_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='Matricule',
        ),
        migrations.RemoveField(
            model_name='utilisateur',
            name='Poste',
        ),
        migrations.RemoveField(
            model_name='utilisateur',
            name='Tel',
        ),
    ]