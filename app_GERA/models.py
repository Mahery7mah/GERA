from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

class Adresse(models.Model):
    ID_Adresse = models.AutoField(primary_key=True)
    Rue = models.CharField(max_length=50)
    ID_Quartier = models.ForeignKey('Quartier', on_delete=models.PROTECT)
    def __str__(self):
        return self.Rue
    class Meta:
        db_table = "Adresse"

class Evenement(models.Model):
    ID_Evenement = models.AutoField(primary_key=True)
    Titre_E = models.CharField(max_length=255, null=True)
    Description_E = models.TextField(null=True)
    Date_Arrive_E = models.DateField(null=True)
    Date_Debut_E = models.DateField(null=True)
    Heure_Debut_E = models.TimeField(null=True)
    Date_Fin_E = models.DateField(null=True)
    Heure_Fin_E = models.TimeField(null=True)
    Publie_E = models.BooleanField(default=None, null=True)
    Image_E = models.ImageField(upload_to='evenement_images/', null=True, blank=True)
    ID_Lieu = models.ForeignKey('Lieu', null=True, on_delete=models.PROTECT)
    ID_Categorie_E = models.ForeignKey('CategorieEvenement', null=True, on_delete=models.CASCADE)
    ID_Interlocuteur = models.ForeignKey('Interlocuteur', null=True, on_delete=models.PROTECT)
    Inscription_E = models.BooleanField(default=None, null=True)
    Date_Limite_Inscription = models.DateField(null=True)
    Est_Fait = models.BooleanField(null=True)
    Num_Audience = models.IntegerField (null = True)
    def __str__(self):
        return self.Titre_E
    class Meta:
        db_table = "Evenement"
        
class Article(models.Model):
    ID_Article = models.AutoField(primary_key=True)
    Titre_Article = models.CharField(max_length=255)
    Contenu_Article = CKEditor5Field('Text', config_name='extends', null=True, blank=True)
    Date_Publication_A = models.DateField()
    Publie_A = models.BooleanField(default=True)
    ID_Auteur = models.ForeignKey('AuteurArticle', on_delete=models.PROTECT)
    ID_Evenement = models.ForeignKey('Evenement', on_delete=models.PROTECT)
    def __str__(self):
        return self.Titre_Article
    def save(self, *args, **kwargs):
        if self.Contenu_Article:
            self.Contenu_Article = self.Contenu_Article.replace('resizeImage:original', 'resizeImage:25')
        super(Article, self).save(*args, **kwargs)
    class Meta:
        db_table = "Article"
        
class AuteurArticle(models.Model):
    ID_Auteur = models.AutoField(primary_key=True)
    Nom_Auteur = models.CharField(max_length=100)
    Prenom_Auteur = models.CharField(max_length=100, null=True)
    def __str__(self):
        return f"{self.Prenom_Auteur} {self.Nom_Auteur}"
    class Meta:
        db_table = "AuteurArticle"

class CategorieEvenement(models.Model):
    ID_Categorie_E = models.AutoField(primary_key=True)
    Categorie_E = models.CharField(max_length=50)
    ID_Type_E = models.ForeignKey('TypeEvenement', on_delete=models.CASCADE)
    def __str__(self):
        return self.Categorie_E
    class Meta:
        db_table = "CategorieEvenement"
        
class InscriptionEvenement(models.Model):
    ID_Membre = models.ForeignKey('Membre', on_delete=models.CASCADE, default='')
    ID_Evenement = models.ForeignKey('Evenement', on_delete=models.CASCADE)
    Date_Inscription_E = models.DateField()
    class Meta:
        unique_together = (('ID_Membre', 'ID_Evenement'),)
        db_table = "InscriptionEvenement"

class Interlocuteur(models.Model):
    ID_Interlocuteur = models.AutoField(primary_key=True)
    Nom_I = models.CharField(max_length=100)
    Prenom_I = models.CharField(max_length=100, null=True)
    Description_I = models.CharField(max_length=255, null=True)
    Mail_I = models.EmailField(null=True, unique=True)
    Tel_I = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return f"{self.Prenom_I} {self.Nom_I}"
    class Meta:
        db_table = "Interlocuteur"

class Lieu(models.Model):
    ID_Lieu = models.AutoField(primary_key=True)
    Lieu = models.CharField(max_length=255)
    Disponibilite_Lieu = models.BooleanField(default=True, null=True)
    Capacite_Lieu = models.IntegerField(null=True)
    ID_Adresse = models.ForeignKey('Adresse', null=True, on_delete=models.PROTECT)
    def __str__(self):
        return self.Lieu
    class Meta:
        db_table = "Lieu"

class Membre(models.Model):
    ID_Membre = models.AutoField(primary_key=True)
    Nom_Utilisateur_M = models.CharField(max_length=50, unique=True, null=True)
    Mot_De_Passe_M = models.CharField(max_length=255, default='', null=True)
    Nom_M = models.CharField(max_length=50, null=True)
    Prenom_M = models.CharField(max_length=50, null=True)
    Matricule_M = models.CharField(max_length=50, null=True)
    Tel_M = models.CharField(max_length=20, null=True)
    Mail_M = models.EmailField(null=True)
    Date_Inscription_M = models.DateField(null=True)
    ID_Poste_P = models.ForeignKey('PosteDuPersonnel', null=True, blank=True, on_delete=models.CASCADE)
    ID_TypeMembre = models.ForeignKey('TypeMembre', on_delete=models.CASCADE, default='')
    def __str__(self):
        return f"{self.Nom_Utilisateur_M}"
    class Meta:
        db_table = "Membre"

class Notification(models.Model):
    ID_Notification = models.AutoField(primary_key=True)
    Message = models.CharField(max_length=255)
    Date_Envoi = models.DateTimeField()
    Est_Lu = models.BooleanField(default=False)
    Est_Lu_Admin = models.BooleanField(default=False)  
    ID_Evenement = models.ForeignKey('Evenement', on_delete=models.CASCADE)
    ID_Membre = models.ForeignKey('Membre', on_delete=models.CASCADE, default='')
    def __str__(self):
        return self.Message
    class Meta:
        db_table = "Notification"

class PosteDuPersonnel(models.Model):
    ID_Poste_P = models.AutoField(primary_key=True)
    Poste_P = models.CharField(max_length=50)
    def __str__(self):
        return self.Poste_P
    class Meta:
        db_table = "PosteDuPersonnel"

class Quartier(models.Model):
    ID_Quartier = models.AutoField(primary_key=True)
    Nom_Quartier = models.CharField(max_length=100)
    ID_Ville = models.ForeignKey('Ville', on_delete=models.PROTECT)
    def __str__(self):
        return self.Nom_Quartier
    class Meta:
        db_table = "Quartier"

class TypeEvenement(models.Model):
    ID_Type_E = models.AutoField(primary_key=True)
    Nom_Type_E = models.CharField(max_length=50)
    def __str__(self):
        return self.Nom_Type_E
    class Meta:
        db_table = "TypeEvenement"

class TypeMembre(models.Model):
    ID_Type_M = models.AutoField(primary_key=True)
    Nom_Type_M = models.CharField(max_length=50)
    def __str__(self):
        return self.Nom_Type_M
    class Meta:
        db_table = "TypeMembre"

class Ville(models.Model):
    ID_Ville = models.AutoField(primary_key=True)
    Nom_Ville = models.CharField(max_length=50)
    CodePostal = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.Nom_Ville} - {self.CodePostal}"
    class Meta:
        db_table = "Ville"
