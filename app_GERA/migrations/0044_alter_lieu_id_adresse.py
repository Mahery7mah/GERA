# Generated by Django 4.2.10 on 2024-05-12 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0043_delete_personnelevenement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lieu',
            name='ID_Adresse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app_GERA.adresse'),
        ),
    ]