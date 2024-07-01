# Generated by Django 4.2.10 on 2024-03-29 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adresse',
            fields=[
                ('ID_Adresse', models.AutoField(primary_key=True, serialize=False)),
                ('Rue', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='AuteurArticle',
            fields=[
                ('ID_Auteur', models.AutoField(primary_key=True, serialize=False)),
                ('Nom', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CategorieEvenement',
            fields=[
                ('ID_Categorie', models.AutoField(primary_key=True, serialize=False)),
                ('Categorie', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('ID_Evenement', models.AutoField(primary_key=True, serialize=False)),
                ('Titre_Evenenement', models.CharField(max_length=255)),
                ('Description_Evenement', models.CharField(max_length=255)),
                ('Date_Heure_Debut', models.DateTimeField()),
                ('Date_Heure_Fin', models.DateTimeField()),
                ('publie', models.BooleanField(default=True)),
                ('Image', models.ImageField(blank=True, null=True, upload_to='evenement_images/')),
                ('ID_Categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_GERA.categorieevenement')),
            ],
        ),
        migrations.CreateModel(
            name='Organisateur',
            fields=[
                ('ID_Organisateur', models.AutoField(primary_key=True, serialize=False)),
                ('Nom', models.CharField(max_length=255)),
                ('Prenom', models.CharField(max_length=255)),
                ('Tel', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PosteDuPersonnel',
            fields=[
                ('ID_Poste', models.AutoField(primary_key=True, serialize=False)),
                ('Poste', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ressource',
            fields=[
                ('ID_Ressource', models.AutoField(primary_key=True, serialize=False)),
                ('Ressource', models.CharField(max_length=255)),
                ('Description_ressource', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('ID_Utilisateur', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ville',
            fields=[
                ('ID_Ville', models.AutoField(primary_key=True, serialize=False)),
                ('Nom', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Quartier',
            fields=[
                ('ID_Quartier', models.AutoField(primary_key=True, serialize=False)),
                ('Nom', models.CharField(max_length=255)),
                ('CodePostal', models.CharField(max_length=20)),
                ('Ville', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_GERA.ville')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('ID_Notification', models.AutoField(primary_key=True, serialize=False)),
                ('Message', models.CharField(max_length=255)),
                ('Date_Envoi', models.DateTimeField()),
                ('Est_Lu', models.BooleanField(default=False)),
                ('ID_Evenement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_GERA.evenement')),
                ('ID_Utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_GERA.utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='Lieu',
            fields=[
                ('ID_Lieu', models.AutoField(primary_key=True, serialize=False)),
                ('Lieu', models.CharField(max_length=255)),
                ('Disponibilite_Lieu', models.BooleanField(default=True)),
                ('Capacite', models.IntegerField()),
                ('Adresse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_GERA.adresse')),
            ],
        ),
        migrations.AddField(
            model_name='evenement',
            name='ID_Lieu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_GERA.lieu'),
        ),
        migrations.AddField(
            model_name='evenement',
            name='ID_Organisateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_GERA.organisateur'),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('ID_Article', models.AutoField(primary_key=True, serialize=False)),
                ('Titre_Artcile', models.CharField(max_length=255)),
                ('Contenu_Article', models.TextField()),
                ('Date_Publication', models.DateField()),
                ('publie', models.BooleanField(default=True)),
                ('ID_Auteur', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_GERA.auteurarticle')),
                ('ID_Evenement', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_GERA.evenement')),
            ],
        ),
        migrations.AddField(
            model_name='adresse',
            name='Quartier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_GERA.quartier'),
        ),
        migrations.CreateModel(
            name='InscriptionEvenement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_Inscription', models.DateField()),
                ('ID_Evenement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_GERA.evenement')),
                ('ID_Utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_GERA.utilisateur')),
            ],
            options={
                'unique_together': {('ID_Utilisateur', 'ID_Evenement')},
            },
        ),
    ]
