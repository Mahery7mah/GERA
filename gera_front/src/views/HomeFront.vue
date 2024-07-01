<template>
  <div>
    <!-- Section Evénement à venir intro -->
    <section id="intro" :style="{ backgroundImage: 'url(' + backgroundImage + ')' }">
      <div class="intro-container wow fadeIn" v-if="prochainEvenement && prochainEvenement.ID_Categorie_E" style="visibility: visible; animation-name: fadeIn;">
        <div class="countdown-container">
          <div v-for="(item, index) in countdown" :key="index" :class="['countdown-circle', { 'countdown-circle-active': item.value > 0 }]" :style="{ animationDelay: item.animationDelay }">
            <div class="countdown-number">{{ item.value }}</div>
            <div class="countdown-label">{{ item.label }}</div>
            <div class="countdown-progress" :style="{ animationDuration: item.animationDuration }"></div>
          </div>
        </div>
        <h1 class="mb-4 pb-0">{{ prochainEvenement.Titre_E }}</h1>
        <p class="mb-4 pb-0">Evénement pour {{ prochainEvenement.ID_Categorie_E.Categorie_E }}</p>
        <a v-if="prochainEvenement && prochainEvenement.ID_Evenement" :href="'/evenement/' + encryptId(prochainEvenement.ID_Evenement)" class="about-btn scrollto">Voir le détail</a>
      </div>
      <div v-else-if="prochainEvenement === null" class="intro-container wow fadeIn" style="visibility: visible; animation-name: fadeIn;">
        <h1 class="mb-4 pb-0">Aucun événement à venir</h1>
      </div>
      <div v-else class="intro-container wow fadeIn" style="visibility: visible; animation-name: fadeIn;">
        <h1 class="mb-4 pb-0">Aucun événement pour le moment</h1>
      </div>
    </section>
    <!-- Section A propos Evenement-->

    <section id="about" v-if="prochainEvenement">
      <div class="container">
        <div class="row">
          <div class="col-lg-6" v-if="prochainEvenement.Description_E">
            <h2><i class="fa fa-info-circle"></i> A propos</h2>
            <p>{{ prochainEvenement.Description_E }}</p>
          </div>
          <div class="col-lg-3" v-if="prochainEvenement.ID_Lieu">
            <h2><i class="fa fa-map-marker"></i> Lieu</h2>
            <p>{{ prochainEvenement.ID_Lieu.Lieu }} Mahamasina</p>
          </div>
          <div class="col-lg-3" v-if="prochainEvenement.Date_Debut_E">
            <h2><i class="fa fa-calendar"></i> Date</h2>
            <p>{{ formatDateTime(prochainEvenement.Date_Debut_E) }}</p>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Section Evénements à venir -->
    <section id="evenement-a-venir" class="schedule section-with-bg">
      <div class="container section-termine wow fadeInUp">
        <div class="section-header">
          <h2 class="text-light">Événements à venir</h2>
        </div>

        <ul class="nav nav-tabs" role="tablist">
          <li class="nav-item">
            <a :class="{ 'nav-link': true, 'active': activeTab === 'personnel' }" @click="activeTab = 'personnel'">Personnel</a>
          </li>
          <li class="nav-item">
            <a :class="{ 'nav-link': true, 'active': activeTab === 'public' }" @click="activeTab = 'public'">Public</a>
          </li>
        </ul>

        <div class="tab-content row justify-content-center">
          <!-- Événements à venir - Personnel -->
          <div v-if="activeTab === 'personnel'" class="col-lg-11 tab-pane fade show active">
            <div v-for="evenement in evenementsAvenirPersonnel.slice(0, 4)" :key="evenement.ID_Evenement" class="row schedule-item">
              <div class="col-md-1"><img class="speaker" :src="getEventImage(evenement.Image_E)" alt="Event Image"></div>
              <div class="col-lg-2">
                <div class="schedule-date">
                  <div class="date-circle blue-circle">{{ formatDateCircle(evenement.Date_Debut_E, 'day') }}</div>
                  <div class="date-circle red-circle">{{ formatDateCircle(evenement.Date_Debut_E, 'month') }}</div>
                  <div class="date-circle green-circle">{{ formatDateCircle(evenement.Date_Debut_E, 'year') }}</div>
                </div>
              </div>
              <div class="col-md-2"><h4>{{ evenement.Titre_E }}</h4></div>
              <div class="col-md-5"><p>{{ truncateDescription(evenement.Description_E) }}</p></div> 
              <div class="col-md-2"><a class="btn btn-link" :href="'/evenement/' + encryptId(evenement.ID_Evenement)">Voir détail</a></div>
            </div>
            <div class="row schedule-item">
              <div class="col text-center">
                <router-link to="/evenements-avenir" class="btn btn-blue text-light">Voir tous les événements à venir</router-link>
              </div>
            </div>
          </div>

          <!-- Événements à venir - Public -->
          <div v-if="activeTab === 'public'" class="col-lg-12 tab-pane fade show active">
            <div v-for="evenement in evenementsAvenirPublic.slice(0, 4)" :key="evenement.ID_Evenement" class="row schedule-item">
              <div class="col-md-1"><img class="speaker" :src="getEventImage(evenement.Image_E)" alt="Event Image"></div>
              <div class="col-lg-2">
                <div class="schedule-date">
                  <div class="date-circle blue-circle">{{ formatDateCircle(evenement.Date_Debut_E, 'day') }}</div>
                  <div class="date-circle red-circle">{{ formatDateCircle(evenement.Date_Debut_E, 'month') }}</div>
                  <div class="date-circle green-circle">{{ formatDateCircle(evenement.Date_Debut_E, 'year') }}</div>
                </div>
              </div>
              <div class="col-md-2"><h4>{{ evenement.Titre_E }}</h4></div>
              <div class="col-md-5"><p>{{ truncateDescription(evenement.Description_E) }}</p></div> 
              <div class="col-md-2"><a class="btn btn-link" :href="'/evenement/' + encryptId(evenement.ID_Evenement)">Voir détail</a></div>
            </div>
            <div class="row schedule-item">
              <div class="col text-center">
                <router-link to="/evenements-avenir" class="btn btn-blue text-light">Voir tous les événements à venir</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section Articles -->
    <section id="articles" class="section-articles" v-if="articles.length > 0">
      <div class="container wow fadeInUp">
        <div class="section-header">
          <h2>Articles Récents</h2>
        </div>
        <div class="row">
          <div class="col-lg-4 mt-4" v-for="article in recentArticles" :key="article.ID_Article">
            <div class="card mb-5 mb-lg-0">
              <img v-if="article.Contenu_Article.includes('<img')" :src="extractImageSrc(article.Contenu_Article)" class="img card-img-top" alt="Article Image">
              <div class="publication-date">
                <div class="date-circle blue-circle">{{ formatDateCircle(article.Date_Publication_A, 'day') }}</div>
                <div class="date-circle red-circle">{{ formatDateCircle(article.Date_Publication_A, 'month') }}</div>
                <div class="date-circle green-circle">{{ formatDateCircle(article.Date_Publication_A, 'year') }}</div>
              </div>
              <div class="card-articles card-body">
                <h5 class="card-title text-muted text-uppercase text-center">{{ article.Titre_Article }}</h5>
                <p class="card-text text-muted" v-html="truncateContent(extractContent(article.Contenu_Article))"></p>
                <hr>
                <div class="text-center">
                  <a :href="'/article/' + encryptId(article.ID_Article)" class="btn article-btn about-btn scrollto">Lire article</a>
                </div> 
              </div>
            </div>
          </div>
        </div>
        <div class="text-center mt-4 mb-5">
          <router-link to="/articles" class="btn btn-blue">Voir tous les articles publiés</router-link>
        </div>
      </div>
    </section>



    <!-- Section Événements terminés -->
    <section id="Evenement-Termnine" class="schedule section-with-bg">
      <div class="container section-event wow fadeInUp">
        <div class="section-header">
          <h2 class="text-light">Événements terminés</h2>
        </div>
        <ul class="nav nav-tabs" role="tablist">
          <li class="nav-item">
            <a :class="{ 'nav-link': true, 'active': activeTab === 'personnel' }" @click="activeTab = 'personnel'">Personnel</a>
          </li>
          <li class="nav-item">
            <a :class="{ 'nav-link': true, 'active': activeTab === 'public' }" @click="activeTab = 'public'">Public</a>
          </li>
        </ul>
        <div class="tab-content row justify-content-center">
          <!-- Événements terminés - Personnel -->
          <div v-if="activeTab === 'personnel'" class="col-lg-11 tab-pane fade show active">
            <div v-for="evenement in evenementsTerminesPersonnel.slice(0, 4)" :key="evenement.ID_Evenement" class="row schedule-item">
              <div class="col-md-1"><img class="speaker" :src="getEventImage(evenement.Image_E)" alt="Event Image"></div>
              <div class="col-lg-2">
                <div class="schedule-date">
                  <div class="date-circle blue-circle">{{ formatDateCircle(evenement.Date_Debut_E, 'day') }}</div>
                  <div class="date-circle red-circle">{{ formatDateCircle(evenement.Date_Debut_E, 'month') }}</div>
                  <div class="date-circle green-circle">{{ formatDateCircle(evenement.Date_Debut_E, 'year') }}</div>
                </div>
              </div>
              <div class="col-md-2"><h4>{{ evenement.Titre_E }}</h4></div>
              <div class="col-md-5"><p>{{ truncateDescription(evenement.Description_E) }}</p></div> 
              <div class="col-md-2"><a class="btn btn-link" :href="'/evenement/' + encryptId(evenement.ID_Evenement)">Voir détail</a></div>
            </div>
            <div class="row schedule-item">
              <div class="col text-center">
                <router-link to="/evenements-termines" class="btn btn-blue text-light">Voir tous les événements terminés</router-link>
              </div>
            </div>
          </div>

          <!-- Événements terminés - Public -->
          <div v-if="activeTab === 'public'" class="col-lg-11 tab-pane fade show active">
            <div v-for="evenement in evenementsTerminesPublic.slice(0, 4)" :key="evenement.ID_Evenement" class="row schedule-item">
              <div class="col-md-1"><img class="speaker" :src="getEventImage(evenement.Image_E)" alt="Event Image"></div>
              <div class="col-lg-2">
                <div class="schedule-date">
                  <div class="date-circle blue-circle">{{ formatDateCircle(evenement.Date_Debut_E, 'day') }}</div>
                  <div class="date-circle red-circle">{{ formatDateCircle(evenement.Date_Debut_E, 'month') }}</div>
                  <div class="date-circle green-circle">{{ formatDateCircle(evenement.Date_Debut_E, 'year') }}</div>
                </div>
              </div>
              <div class="col-md-2"><h4>{{ evenement.Titre_E }}</h4></div>
              <div class="col-md-5"><p>{{ truncateDescription(evenement.Description_E) }}</p></div> 
              <div class="col-md-2"><a class="btn btn-link" :href="'/evenement/' + encryptId(evenement.ID_Evenement)">Voir détail</a></div>
            </div>
            <div class="row schedule-item">
              <div class="col text-center">
                <router-link to="/evenements-termines" class="btn btn-blue text-light">Voir tous les événements terminés</router-link>
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
      return `/static${this.prochainEvenement.Image_E}`;
    } else {
      return '/static/img/default-bg.jpg'; // Image de fond par défaut si aucune image n'est définie pour l'événement
    }
  },
  recentArticles() {
      return this.articles.slice(0, 3);
    },
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
        });

        // Trier les articles par date de publication décroissante
        this.articles = articles.sort((a, b) => new Date(b.Date_Publication_A) - new Date(a.Date_Publication_A));
      } catch (error) {
        console.error('Erreur lors de la récupération des articles:', error);
      }
    },
    truncateContent(content) {
      return content.length > 150 ? content.substring(0, 150) + '...' : content;
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
      return imagePath ? `http://127.0.0.1:8000/static${imagePath}` : ''; // Modifier l'URL selon vos besoins
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    }
  }
};
</script>

<style>

</style>