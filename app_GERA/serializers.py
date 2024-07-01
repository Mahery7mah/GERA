from rest_framework import serializers
from .models import Ville, Evenement, Membre, PosteDuPersonnel, TypeMembre, Article, CategorieEvenement, Lieu, Notification
from django.contrib.auth.hashers import make_password


class LieuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lieu
        fields = ['ID_Lieu', 'Lieu']

class CategorieEvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieEvenement
        fields = ['ID_Categorie_E', 'Categorie_E']

class VilleSerializer(serializers.ModelSerializer) : 
    class Meta:
        model = Ville
        fields = '__all__'
        
class ProchainEvenementSerializer(serializers.ModelSerializer):
    ID_Lieu = LieuSerializer()
    ID_Categorie_E = CategorieEvenementSerializer()
    
    class Meta:
        model = Evenement
        fields = '__all__'
        
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        
class PersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membre
        fields = ['Nom_Utilisateur_M', 'Mot_De_Passe_M', 'Matricule_M', 'Mail_M', 'Tel_M']


    def validate(self, data):
        # Vérifiez si le matricule correspond à un membre de type "personnel"
        matricule = data.get('Matricule_M')
        try:
            membre = Membre.objects.get(Matricule_M=matricule, ID_TypeMembre='membre_personnel')
        except Membre.DoesNotExist:
            raise serializers.ValidationError("Matricule invalide")
        
        return data
class MembreSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membre
        fields = ['Nom_Utilisateur_M', 'Mot_De_Passe_M', 'Nom_M', 'Prenom_M', 'Tel_M', 'Mail_M', 'ID_TypeMembre']
        
        
class EvenementSerializer(serializers.ModelSerializer):
    ID_Lieu = LieuSerializer()
    ID_Categorie_E = CategorieEvenementSerializer()
    class Meta:
        model = Evenement
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    evenement_titre = serializers.CharField(source='ID_Evenement.Titre_E', read_only=True)
    evenement_image = serializers.ImageField(source='ID_Evenement.Image_E', read_only=True)
    class Meta:
        model = Notification
        fields = '__all__'