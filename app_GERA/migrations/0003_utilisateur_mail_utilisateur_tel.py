# Generated by Django 4.2.10 on 2024-03-30 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0002_utilisateur_matricule_personnel'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='Mail',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='Tel',
            field=models.CharField(max_length=20, null=True),
        ),
    ]