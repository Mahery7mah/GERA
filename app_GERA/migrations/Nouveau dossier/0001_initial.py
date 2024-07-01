# Generated by Django 4.2.10 on 2024-03-29 15:56

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
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
            name='Ville',
            fields=[
                ('ID_Ville', models.AutoField(primary_key=True, serialize=False)),
                ('Nom', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('Matricule', models.CharField(max_length=20, unique=True)),
                ('Tel', models.CharField(max_length=20, unique=True)),
                ('Poste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_GERA.postedupersonnel')),
                ('groups', models.ManyToManyField(blank=True, related_name='user_custom_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_custom_set', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
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
