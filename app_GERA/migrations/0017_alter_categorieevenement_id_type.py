# Generated by Django 4.2.10 on 2024-04-04 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_GERA', '0016_remove_evenement_id_type_categorieevenement_id_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorieevenement',
            name='ID_Type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_GERA.typeevenement'),
        ),
    ]
