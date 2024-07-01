# Generated by Django 4.2.10 on 2024-04-04 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0014_alter_evenement_date_heure_debut_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeEvenement',
            fields=[
                ('ID_Type', models.AutoField(primary_key=True, serialize=False)),
                ('Nom_Type', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='evenement',
            name='ID_Type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_GERA.typeevenement'),
        ),
    ]
