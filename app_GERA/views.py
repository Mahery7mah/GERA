from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Ville, Quartier, Adresse, Evenement, Membre, PosteDuPersonnel, TypeMembre, Article, InscriptionEvenement, Notification
from .serializers import VilleSerializer, ProchainEvenementSerializer, MembreSimpleSerializer, ArticleSerializer, EvenementSerializer, NotificationSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from django.db import transaction
from rest_framework.permissions import IsAuthenticated  # Added for authentication

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout


from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from datetime import datetime

from django.utils import timezone  # Utiliser timezone pour obtenir la date actuelle avec le fuseau horaire correct

import pytz


# from .serializers import VilleSerializer


@csrf_exempt
def ville_list(request):
    if request.method == 'GET':
        villes = Ville.objects.all()
        serializer = VilleSerializer(villes, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = VilleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def ville_detail(request, pk):
    try:
        ville = Ville.objects.get(pk=pk)
    except Ville.DoesNotExist:
        return JsonResponse({'error': 'La ville n\'existe pas.'}, status=404)

    if request.method == 'GET':
        serializer = VilleSerializer(ville)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = VilleSerializer(ville, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        ville.delete()
        return JsonResponse({'message': 'La ville a été supprimée avec succès.'}, status=204)


@api_view(['GET'])
def prochain_evenement(request):
    prochains_evenements = Evenement.objects.filter(Publie_E=True).order_by('Date_Debut_E')
    serializer = ProchainEvenementSerializer(prochains_evenements, many=True)
    return Response(serializer.data)

class VilleViewSet(viewsets.ModelViewSet):
    queryset = Ville.objects.all()
    serializer_class = VilleSerializer
    


@api_view(['POST'])
def register_personnel(request):
    if request.method == 'POST':
        try:
            matricule = request.data.get('Matricule_M', None)
            nom_utilisateur = request.data.get('Nom_Utilisateur_M', None)
            mot_de_passe = request.data.get('Mot_De_Passe_M', None)

            if matricule and nom_utilisateur and mot_de_passe:
                personnel = get_object_or_404(Membre, Matricule_M=matricule)
                type_membre = get_object_or_404(TypeMembre, Nom_Type_M='membre_personnel')
                # Mise à jour du nom d'utilisateur et du mot de passe du personnel
                personnel.Nom_Utilisateur_M = nom_utilisateur
                personnel.Mot_De_Passe_M = make_password(mot_de_passe)
                personnel.ID_TypeMembre = type_membre
                personnel.save()
                
                return Response({'message': 'Inscription du personnel réussie.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Données incomplètes'}, status=status.HTTP_400_BAD_REQUEST)
        except Membre.DoesNotExist:
            return Response({'error': 'Matricule_M invalide'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Erreur interne du serveur: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Méthode non autorisée'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def register_utilisateur_simple(request):
    if request.method == 'POST':
        serializer = MembreSimpleSerializer(data=request.data)
        if serializer.is_valid():
            # Ajouter automatiquement le type de membre "membre_simple"
            type_membre = get_object_or_404(TypeMembre, Nom_Type_M='membre_simple')
            serializer.validated_data['ID_TypeMembre'] = type_membre
            
            # Hasher le mot de passe avant de l'enregistrer
            serializer.validated_data['Mot_De_Passe_M'] = make_password(serializer.validated_data['Mot_De_Passe_M'])
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def member_login(request):
    if request.method == 'POST':
        username = request.data.get('Nom_Utilisateur_M')
        password = request.data.get('Mot_De_Passe_M')
        
        # Recherche de l'utilisateur par nom d'utilisateur
        try:
            member = Membre.objects.get(Nom_Utilisateur_M=username)
        except Membre.DoesNotExist:
            return JsonResponse({'error': 'Nom d\'utilisateur incorrect'}, status=400)

        # Vérification du mot de passe
        if check_password(password, member.Mot_De_Passe_M):
            # Authentification réussie
            request.session['member_id'] = member.pk  # Save the member id in the session
            return JsonResponse({'message': 'Connexion réussie.', 'username': member.Nom_Utilisateur_M, 'member_id': member.pk})
        else:
            # Mot de passe incorrect
            return JsonResponse({'error': 'Mot de passe incorrect'}, status=400)

@api_view(['POST'])
def member_logout(request):
    if request.method == 'POST':
        try:
            del request.session['member_id']  # Delete the member id from the session
        except KeyError:
            pass
        return JsonResponse({'message': 'Déconnexion réussie.'})

@api_view(['GET'])
def check_login(request):
    if request.method == 'GET':
        member_id = request.session.get('member_id')
        if member_id:
            member = Membre.objects.get(pk=member_id)
            return JsonResponse({'username': member.Nom_Utilisateur_M})
        else:
            return JsonResponse({'error': 'Utilisateur non connecté'}, status=400)

@api_view(['GET'])
def evenement_detail(request, pk):
    try:
        evenement = Evenement.objects.get(pk=pk)
        serializer = ProchainEvenementSerializer(evenement)
        return Response(serializer.data)
    except Evenement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_published_articles(request):
    articles = Article.objects.filter(Publie_A=True)
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def evenements_personnel(request):
    evenements = Evenement.objects.filter(ID_Categorie_E__Categorie_E='personnel')
    serializer = EvenementSerializer(evenements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def evenements_public(request):
    try :
        evenements = Evenement.objects.filter(ID_Categorie_E__Categorie_E='public')
        serializer = EvenementSerializer(evenements, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': 'Erreur interne du serveur: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET', 'POST'])
def inscription_evenement(request, pk):
    if request.method == 'POST':
        # Vérifier si l'utilisateur est connecté
        member_id = request.session.get('member_id')
        if not member_id:
            return JsonResponse({'error': 'Veuillez vous connecter d\'abord avant de vous inscrire sur cet événement'}, status=400)

        try:
            # Récupérer l'utilisateur connecté
            member = Membre.objects.get(pk=member_id)
        except Membre.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=400)

        # Vérifier si l'événement existe
        try:
            evenement = Evenement.objects.get(pk=pk)
        except Evenement.DoesNotExist:
            return JsonResponse({'error': 'Événement non trouvé'}, status=400)

        # Vérifier si l'événement est déjà terminé
        now = timezone.now().date()
        if evenement.Date_Debut_E < now:
            return JsonResponse({'error': 'Cet événement est déjà terminé, vous ne pouvez pas vous inscrire'}, status=400)

        # Vérifier le type de membre
        if member.ID_TypeMembre.Nom_Type_M == 'membre_simple' and evenement.ID_Categorie_E.Categorie_E != 'public':
            return JsonResponse({'error': 'Vous ne pouvez pas vous inscrire à cet événement'}, status=400)

        try:
            # Créer une nouvelle inscription à l'événement
            inscription = InscriptionEvenement.objects.create(
                ID_Membre=member,
                ID_Evenement=evenement,
                Date_Inscription_E=timezone.now()
            )
            inscription.save()
            return JsonResponse({'message': 'Vous êtes inscrit à cet événement'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def get_notifications(request):
    member_id = request.session.get('member_id')
    if member_id:
        notifications = Notification.objects.filter(ID_Membre=member_id).order_by('-Date_Envoi')
        serializer = NotificationSerializer(notifications, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Utilisateur non connecté'}, status=400)

@api_view(['POST'])
def mark_all_as_read(request):
    member_id = request.session.get('member_id')
    if member_id:
        Notification.objects.filter(ID_Membre=member_id, Est_Lu=False).update(Est_Lu=True)
        return JsonResponse({'message': 'Toutes les notifications ont été marquées comme lues.'})
    else:
        return JsonResponse({'error': 'Utilisateur non connecté'}, status=400)