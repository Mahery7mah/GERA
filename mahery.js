
Alors pour une application de gestion des événements avec redaction des articles avec backend et frontend django, j'ai utilisé l'application classique de django pour le backend(coté admin pour la gestion) et je vais utiliser l'application vue.js pour le frontend(coté client comme un site)

extrait de urls.py : 

    #api frontend
    
    #villes
    path('api/ville-list/', app_GERA.ville_list, name='ville_list'),
    path('api/ville-detail/<int:pk>/', app_GERA.ville_detail, name='ville_detail'),
    
    #événements
    path('api/prochain-evenement/', app_GERA.prochain_evenement, name='prochain-evenement'),
    # path('api/inscription/Personnel/<str:matricule>/check/', app_GERA.check_matricule_existence, name='check_matricule_existence'),
    path('api/articles/', app_GERA.get_published_articles, name='get_published_articles'),
    path('api/evenement-detail/<int:pk>/', app_GERA.evenement_detail, name='evenement_detail'),
    path('api/article-detail/<int:pk>/', app_GERA.article_detail, name='article_detail'),
    #Inscription :
    # path('api/inscription/personnel/', app_GERA.register_personnel, name='register_personnel'),
    # Connexion
    path('api/login/', app_GERA.member_login, name='login'),
    path('api/logout/', app_GERA.member_logout, name='logout'),
    path('api/check_login/', app_GERA.check_login, name='member_check_login'),

    path('api/inscription/personnel/', app_GERA.register_personnel, name='register_personnel'),

    # path('api/inscription/personnel/', app_GERA.register_personnel, name='register_personnel'),
    path('api/inscription/membre-simple/', app_GERA.register_utilisateur_simple, name='register_utilisateur_simple'),

    path('api/evenements_personnel/', app_GERA.evenements_personnel, name='evenements_personnel'),
    path('api/evenements_public/', app_GERA.evenements_public, name='evenements_public'),
    # path('api/inscription-evenement/', app_GERA.inscription_evenement, name='inscription_evenement'),
    path('api/inscription-evenement/<int:pk>/', app_GERA.inscription_evenement, name='inscription_evenement'),


extrait de models.py :
from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

class Evenement(models.Model):
    ID_Evenement = models.AutoField(primary_key=True)
    Titre_E = models.CharField(max_length=255, null=True)
    Description_E = models.CharField(max_length=255, null=True)
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
    Prenom_Auteur = models.CharField(max_length=100)
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

serializers.py : 
from rest_framework import serializers
from .models import Ville, Evenement, Membre, PosteDuPersonnel, TypeMembre, Article, CategorieEvenement, Lieu
from django.contrib.auth.hashers import make_password

class MembreSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membre
        fields = ['Nom_Utilisateur', 'Mot_De_Passe', 'Nom', 'Prenom', 'Tel', 'Type_Membre']
        

views.py : 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Ville, Quartier, Adresse, Evenement, Membre, PosteDuPersonnel, TypeMembre, Article
from .serializers import VilleSerializer, ProchainEvenementSerializer, MembreSimpleSerializer, ArticleSerializer, EvenementSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from django.db import transaction
from rest_framework.permissions import IsAuthenticated  # Added for authentication

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login


from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from datetime import datetime

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


gera_front/public/index.html :
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <div id="app">
  </div>
</body>
</html>

gera_front/src/main.js :
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const app = createApp(App);

app.use(router);

app.mount("#app");


gera_front/vue.config.js :
module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        logLevel: 'debug',
        pathRewrite: { '^/api': '/api' },
      },
    },
  },
  css: {
    loaderOptions: {
      sass: {
        additionalData: @import "@/assets/styles/_variables.scss";
      }
    }
  }
};


src/App.vue :
<template>
  <div id="app">
    <Header />
    <router-view />
    <Footer />
  </div>
</template>

<script>
import Header from './components/HeaderFront.vue';
import Footer from './components/FooterFront.vue';

export default {
  components: {
    Header,
    Footer
  },
  // Comportements
}
</script>

<style lang="scss">
/* Styles Sass pour l'application principale */
</style>

router.js : 
import { createRouter, createWebHistory } from 'vue-router';
import HomeFront from './views/HomeFront.vue'; // Importez la vue HomeFront.vue
import SelectionUtilisateur from './views/SelectionUtilisateur.vue';
import UtilisateurSimpleForm from './views/UtilisateurSimpleForm.vue';
import PersonnelForm from './views/PersonnelForm.vue';
import ConnexionForm from './views/ConnexionForm.vue';
import DetailEvenement from './views/DetailEvenement.vue';
import DetailArticle from './views/DetailArticle.vue';


import { decryptId } from './utils'; // Importez la fonction decryptId depuis votre fichier utils.js

const routes = [
  {
    path: '/',
    name: 'HomeFront',
    component: HomeFront,
  },

  {
    path: '/inscription',
    name: 'SelectionUtilisateur',
    component: SelectionUtilisateur,
  },
  {
    path: '/inscription/utilisateur-simple',
    name: 'UtilisateurSimpleForm',
    component: UtilisateurSimpleForm,
  },
  {
    path: '/inscription/personnel',
    name: 'PersonnelForm',
    component: PersonnelForm,
  },  
  {
    path: '/connexion',
    name: 'ConnexionForm',
    component: ConnexionForm,
  },


];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

HeaderFront.vue : 
<template>
  <div>
    <!-- Section Articles -->
    <section id="articles" class="" v-if="articles.length > 0">
      <div class="container wow fadeInUp">
        <div class="section-header">
          <h2>Articles</h2>
        </div>
        <div class="row">
          <div class="col-lg-4" v-for="article in articles" :key="article.ID_Article">
            <div class="card mb-5 mb-lg-0">
              <img v-if="article.Contenu_Article.includes('<img')" :src="extractImageSrc(article.Contenu_Article)" class="img card-img-top" alt="Article Image">
              <div class="publication-date">
                  <div class="date-circle blue-circle">{{ formatDateCircle(article.Date_Publication_A, 'day') }}</div>
                  <div class="date-circle red-circle">{{ formatDateCircle(article.Date_Publication_A, 'month') }}</div>
                  <div class="date-circle green-circle">{{ formatDateCircle(article.Date_Publication_A, 'year') }}</div>
                </div>
              <div class="card-body">
                <!-- Placement du texte Date_Publication -->
                <h5 class="card-title text-muted text-uppercase text-center">{{ article.Titre_Article }}</h5>
                <p class="card-text text-muted" v-html="truncateContent(extractContent(article.Contenu_Article))"></p>
                <hr>
                <div class="text-center">
                  <a :href="'/article/' + encryptId(article.ID_Article)" class="btn about-btn scrollto">Lire article</a>
                </div> 
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>



  </div>
</template>

<script>
import { encryptId } from '../utils';

export default {
  data() {
    return {
      prochainEvenement: null,
      countdown: {
        days: 0,
        hours: 0,
        minutes: 0,
        seconds: 0
      },
      activeTab: 'personnel', // onglet actif par défaut

      articles: [],
      evenementsAvenirPersonnel: [],
      evenementsAvenirPublic: [],
      evenementsTerminesPersonnel: [], 
      evenementsTerminesPublic: [],
    };
  },
  computed: {
  backgroundImage() {
    if (this.prochainEvenement && this.prochainEvenement.Image_E) {
      return /static${this.prochainEvenement.Image_E};
    } else {
      return '/static/img/default-bg.jpg'; // Image de fond par défaut si aucune image n'est définie pour l'événement
    }
  }
  },
  created() {
    this.fetchProchainEvenement();
    this.fetchArticles();
    this.fetchEvenementsAvenirPersonnel();
    this.fetchEvenementsAvenirPublic();
    this.fetchEvenementsTerminesPersonnel();
    this.fetchEvenementsTerminesPublic();
  },
  mounted() {
    this.countdownInterval = setInterval(this.updateCountdown, 1000);
  },
  beforeUnmount() {
    clearInterval(this.countdownInterval);
  },
  methods: {
    async fetchEvenementsAvenirPersonnel() {
      try {
        const response = await fetch('/api/evenements_personnel/');
        const evenements = await response.json();
        this.evenementsAvenirPersonnel = evenements.filter(evenement => new Date(evenement.Date_Debut_E) >= new Date());
      } catch (error) {
        console.error('Erreur lors de la récupération des événements à venir du personnel:', error);
      }
    },
    async fetchEvenementsAvenirPublic() {
      try {
        const response = await fetch('/api/evenements_public/');
        const evenements = await response.json();
        this.evenementsAvenirPublic = evenements.filter(evenement => new Date(evenement.Date_Debut_E) >= new Date());
      } catch (error) {
        console.error('Erreur lors de la récupération des événements à venir du public:', error);
      }
    },
    async fetchEvenementsTerminesPersonnel() {
      try {
        const response = await fetch('/api/evenements_personnel/');
        const evenements = await response.json();
        this.evenementsTerminesPersonnel = evenements.filter(evenement => new Date(evenement.Date_Debut_E) < new Date());
      } catch (error) {
        console.error('Erreur lors de la récupération des événements à venir du personnel:', error);
      }
    },
    async fetchEvenementsTerminesPublic() {
      try {
        const response = await fetch('/api/evenements_public/');
        const evenements = await response.json();
        this.evenementsTerminesPublic = evenements.filter(evenement => new Date(evenement.Date_Debut_E) < new Date());
      } catch (error) {
        console.error('Erreur lors de la récupération des événements à venir du public:', error);
      }
    },
    truncateDescription(description) {
      return description.length > 100 ? description.substring(0, 100) + '...' : description;
    },
    async fetchProchainEvenement() {
      try {
        const response = await fetch('/api/prochain-evenement/');
        const prochainsEvenements = await response.json();
        if (prochainsEvenements.length > 0) {
          this.prochainEvenement = prochainsEvenements.find(evenement => new Date(evenement.Date_Debut_E) >= new Date());
          if (this.prochainEvenement) {
            this.updateCountdown();
          }
        } else {
          this.prochainEvenement = null;
        }
      } catch (error) {
        console.error('Erreur lors de la récupération du prochain événement:', error);
      }
    },
    async fetchArticles() {
      try {
        const response = await fetch('/api/articles/');
        const articles = await response.json();

        articles.forEach(article => {
          article.Contenu_Article = article.Contenu_Article.replace(/src="/g, 'src="http://localhost:8000');
          // article.Contenu_Article = article.Contenu_Article.replace(/<img/g, '<img style="height: 50px !important; width: 60px !important;"');
        });

        this.articles = articles;
      } catch (error) {
        console.error('Erreur lors de la récupération des articles:', error);
      }
    },
    truncateContent(content) {
      return content.length > 70 ? content.substring(0, 100) + '...' : content;
    },
    extractContent(content) {
      return content.replace(/<[^>]+>/g, '');
    },
    extractImageSrc(content) {
      const regex = /<img.*?src=["'](.*?)["']/;
      const match = regex.exec(content);
      if (match && match[1]) {
        return match[1];
      } else {
        return '';
      }
    },
    updateCountdown() {
      if (this.prochainEvenement) {
        const now = new Date();
        const eventDate = new Date(this.prochainEvenement.Date_Debut_E);
        const difference = eventDate.getTime() - now.getTime();

        this.countdown = [
          { value: Math.floor(difference / (1000 * 60 * 60 * 24)), label: 'Jours' },
          { value: Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)), label: 'Heures' },
          { value: Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60)), label: 'Minutes' },
          { value: Math.floor((difference % (1000 * 60)) / 1000), label: 'Secondes' }
        ];
      }
    },
    formatDateTime(dateTime) {
      return new Date(dateTime).toLocaleString();
    },
    formatDateCircle(date, part) {
  const d = new Date(date);
  switch(part) {
    case 'day':
      return d.getDate();
    case 'month':
      return d.getMonth() + 1;
    case 'year':
      return d.getFullYear();
    default:
      return '';
  }
},
    encryptId(id) {
      return encryptId(id);
    },
     getEventImage(imagePath) {
      return imagePath ? http://127.0.0.1:8000/static${imagePath} : ''; // Modifier l'URL selon vos besoins
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    }
  }
};
</script>

Nouvelle fonctionnalité à mettre à jour : 
Afficher seulement les 3 articles récentes (Date_Publication_A) sur la section article dans HomeFront.vue
Et ajouter au dessous des cards des articles dans HomeFront.vue un lien qui permet de voir tout les articles publiés(donc une autre page pour cela ArticlePublie.vue)
Donc veuillez donner seulement toutes les parties du code de HomeFront.vue à ajouter et le code au grand complet sans exception de ArticlePublie.vue avec les style et tout, bien responsive et la place des cards bien toujours au centre quand ils depasse meme de 3, veuillez donner ces codes pour faire tout ces fonctionnalité au grand complet sans exception s'il vous plait.

ChatGPT
Pour implémenter les fonctionnalités demandées, nous allons procéder en deux étapes :

Modifier HomeFront.vue pour n'afficher que les trois articles les plus récents et ajouter un lien pour voir tous les articles publiés.
Créer un nouveau composant ArticlePublie.vue pour afficher tous les articles publiés.
Voici les modifications et ajouts nécessaires.

1. Modification de HomeFront.vue
Template
vue
Copier le code
<template>
  <div id="app">
    <Header />
    <section id="articles" class="section-articles" v-if="articles.length > 0">
      <div class="container wow fadeInUp">
        <div class="section-header">
          <h2>Articles Récents</h2>
        </div>
        <div class="row">
          <div class="col-lg-4" v-for="article in recentArticles" :key="article.ID_Article">
            <div class="card mb-5 mb-lg-0">
              <img v-if="article.Contenu_Article.includes('<img')" :src="extractImageSrc(article.Contenu_Article)" class="img card-img-top" alt="Article Image">
              <div class="publication-date">
                <div class="date-circle blue-circle">{{ formatDateCircle(article.Date_Publication_A, 'day') }}</div>
                <div class="date-circle red-circle">{{ formatDateCircle(article.Date_Publication_A, 'month') }}</div>
                <div class="date-circle green-circle">{{ formatDateCircle(article.Date_Publication_A, 'year') }}</div>
              </div>
              <div class="card-body">
                <h5 class="card-title text-muted text-uppercase text-center">{{ article.Titre_Article }}</h5>
                <p class="card-text text-muted" v-html="truncateContent(extractContent(article.Contenu_Article))"></p>
                <hr>
                <div class="text-center">
                  <a :href="'/article/' + encryptId(article.ID_Article)" class="btn about-btn scrollto">Lire article</a>
                </div> 
              </div>
            </div>
          </div>
        </div>
        <div class="text-center mt-4">
          <router-link to="/articles" class="btn btn-primary">Voir tous les articles publiés</router-link>
        </div>
      </div>
    </section>
    <router-view />
    <Footer />
  </div>
</template>
Script
vue
Copier le code
<script>
import { encryptId } from '../utils';
import Header from './HeaderFront.vue';
import Footer from './FooterFront.vue';

export default {
  components: {
    Header,
    Footer
  },
  data() {
    return {
      articles: [],
      // autres données
    };
  },
  computed: {
    recentArticles() {
      return this.articles.slice(0, 3);
    },
  },
  created() {
    this.fetchArticles();
    // autres méthodes fetch
  },
  methods: {
    async fetchArticles() {
      try {
        const response = await fetch('/api/articles/');
        const articles = await response.json();

        articles.forEach(article => {
          article.Contenu_Article = article.Contenu_Article.replace(/src="/g, 'src="http://localhost:8000');
        });

        // Trier les articles par date de publication décroissante
        this.articles = articles.sort((a, b) => new Date(b.Date_Publication_A) - new Date(a.Date_Publication_A));
      } catch (error) {
        console.error('Erreur lors de la récupération des articles:', error);
      }
    },
    truncateContent(content) {
      return content.length > 100 ? content.substring(0, 100) + '...' : content;
    },
    extractContent(content) {
      return content.replace(/<[^>]+>/g, '');
    },
    extractImageSrc(content) {
      const regex = /<img.*?src=["'](.*?)["']/;
      const match = regex.exec(content);
      return match ? match[1] : '';
    },
    encryptId(id) {
      return encryptId(id);
    }
  }
};
</script>
Styles
vue
Copier le code
<style lang="scss">
/* Styles Sass pour l'application principale */
.section-articles .card {
  margin: 0 auto; /* Centrer les cards */
}
.text-center {
  text-align: center;
}
.mt-4 {
  margin-top: 1.5rem;
}
</style>
2. Création de ArticlePublie.vue
Créez un nouveau fichier ArticlePublie.vue dans le dossier views.

vue
Copier le code
<template>
  <div class="container">
    <div class="section-header">
      <h2>Tous les Articles Publiés</h2>
    </div>
    <div class="row">
      <div class="col-lg-4" v-for="article in articles" :key="article.ID_Article">
        <div class="card mb-5 mb-lg-0">
          <img v-if="article.Contenu_Article.includes('<img')" :src="extractImageSrc(article.Contenu_Article)" class="img card-img-top" alt="Article Image">
          <div class="publication-date">
            <div class="date-circle blue-circle">{{ formatDateCircle(article.Date_Publication_A, 'day') }}</div>
            <div class="date-circle red-circle">{{ formatDateCircle(article.Date_Publication_A, 'month') }}</div>
            <div class="date-circle green-circle">{{ formatDateCircle(article.Date_Publication_A, 'year') }}</div>
          </div>
          <div class="card-body">
            <h5 class="card-title text-muted text-uppercase text-center">{{ article.Titre_Article }}</h5>
            <p class="card-text text-muted" v-html="truncateContent(extractContent(article.Contenu_Article))"></p>
            <hr>
            <div class="text-center">
              <a :href="'/article/' + encryptId(article.ID_Article)" class="btn about-btn scrollto">Lire article</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { encryptId } from '../utils';

export default {
  data() {
    return {
      articles: []
    };
  },
  created() {
    this.fetchArticles();
  },
  methods: {
    async fetchArticles() {
      try {
        const response = await fetch('/api/articles/');
        const articles = await response.json();

        articles.forEach(article => {
          article.Contenu_Article = article.Contenu_Article.replace(/src="/g, 'src="http://localhost:8000');
        });

        // Trier les articles par date de publication décroissante
        this.articles = articles.sort((a, b) => new Date(b.Date_Publication_A) - new Date(a.Date_Publication_A));
      } catch (error) {
        console.error('Erreur lors de la récupération des articles:', error);
      }
    },
    truncateContent(content) {
      return content.length > 100 ? content.substring(0, 100) + '...' : content;
    },
    extractContent(content) {
      return content.replace(/<[^>]+>/g, '');
    },
    extractImageSrc(content) {
      const regex = /<img.*?src=["'](.*?)["']/;
      const match = regex.exec(content);
      return match ? match[1] : '';
    },
    formatDateCircle(date, part) {
      const d = new Date(date);
      switch (part) {
        case 'day':
          return d.getDate();
        case 'month':
          return d.getMonth() + 1;
        case 'year':
          return d.getFullYear();
        default:
          return '';
      }
    },
    encryptId(id) {
      return encryptId(id);
    }
  }
};
</script>

<style lang="scss">
/* Styles pour la page de tous les articles */
.section-header {
  text-align: center;
  margin-bottom: 2rem;
}
.card {
  margin: 0 auto; /* Centrer les cards */
}
</style>
3. Mise à jour du routeur
Ajoutez une nouvelle route pour ArticlePublie.vue dans router.js.

js
Copier le code
import { createRouter, createWebHistory } from 'vue-router';
import HomeFront from './views/HomeFront.vue';
import SelectionUtilisateur from './views/SelectionUtilisateur.vue';
import UtilisateurSimpleForm from './views/UtilisateurSimpleForm.vue';
import PersonnelForm from './views/PersonnelForm.vue';
import ConnexionForm from './views/ConnexionForm.vue';
import DetailEvenement from './views/DetailEvenement.vue';
import DetailArticle from './views/DetailArticle.vue';
import ArticlePublie from './views/ArticlePublie.vue'; // Import de la nouvelle vue

const routes = [
  {
    path: '/',
    name: 'HomeFront',
    component: HomeFront,
  },
  {
    path: '/inscription',
    name: 'SelectionUtilisateur',
    component: SelectionUtilisateur,
  },
  {
    path: '/inscription/utilisateur-simple',
    name: 'UtilisateurSimpleForm',
    component: UtilisateurSimpleForm,
  },
  {
    path: '/inscription/personnel',
    name: 'PersonnelForm',
    component: PersonnelForm,
  },
  {
    path: '/connexion',
    name: 'ConnexionForm',
    component: ConnexionForm,
  },
  {
    path: '/articles',
    name: 'ArticlePublie',
    component: ArticlePublie, // Définition de la route pour tous les articles publiés
  },
  {
    path: '/evenement/:id',
    name: 'DetailEvenement',
    component: DetailEvenement,
  },
  {
    path: '/article/:id',
    name: 'DetailArticle',
    component: DetailArticle,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
Conclusion
Ces modifications permettent de n'afficher que les trois articles les plus récents sur la page d'accueil, avec un lien vers une nouvelle page qui liste tous les articles publiés. Ces pages sont respectivement HomeFront.vue et ArticlePublie.vue. Le routeur est mis à jour pour inclure la nouvelle route /articles.







Message ChatGPT

ChatGPT peut faire des erreurs. Envisagez de vérifier les informations importantes.
?
ChatGPT
