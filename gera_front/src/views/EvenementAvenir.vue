<template>
    <!-- Section Événements à venir -->
    <section id="evenement-a-venir" class="schedule section-with-bg">
      <div class="container section-termine wow fadeInUp">
        <div class="section-header mt-5">
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
            <div v-for="evenement in evenementsAvenirPersonnel" :key="evenement.ID_Evenement" class="row schedule-item">
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
          </div>

          <!-- Événements à venir - Public -->
          <div v-if="activeTab === 'public'" class="col-lg-12 tab-pane fade show active">
            <div v-for="evenement in evenementsAvenirPublic" :key="evenement.ID_Evenement" class="row schedule-item">
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
          </div>
        </div>
      </div>
    </section>
</template>

<script>
import { encryptId } from '../utils';

export default {
  data() {
    return {
      activeTab: 'personnel', // onglet actif par défaut

      evenementsAvenirPersonnel: [],
      evenementsAvenirPublic: [],
    };
  },
  created() {
    this.fetchEvenementsAvenirPersonnel();
    this.fetchEvenementsAvenirPublic();
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
    truncateDescription(description) {
      return description.length > 100 ? description.substring(0, 100) + '...' : description;
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
  }
};
</script>