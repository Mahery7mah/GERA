<template>
  <section id="speakers-details" class="section-auth wow fadeIn">
    <div class="container" v-if="evenement">
      <div class="section-header">
        <h2>{{ evenement.Titre_E }}</h2>
        <p>{{ evenement.Date_Debut_E }}</p>
        <div class="row justify-content-center text-center">

        </div>
      </div>
  
        <div class="row" v-if="evenement.ID_Lieu">
          <div class="col-md-6">
            <img :src="getEventImage(evenement.Image_E)" alt="Image de l'événement" class="img-fluid">
          </div>
  
          <div class="col-md-6">
            <div class="details">
              <div class="countdown mb-4 pb-0" v-if="evenement.Date_Debut_E">
                <div class="timer-detail" v-if="countdown.days >= 0">
                  <span id="days" class="text-primary"><i class="fa fa-calendar"></i>  Dans {{ countdown.days }}jours </span> 
                  <span id="hours" class="text-primary">{{ countdown.hours }}heures </span> 
                  <span id="minutes" class="text-primary">{{ countdown.minutes }}minutes </span> 
                  <span id="seconds" class="text-primary">{{ countdown.seconds }}secondes </span> 
                </div>
                <div v-else>
                  <h5 class="text-danger">Événement terminé</h5> 
                </div>
              </div>
              <p>{{ evenement.Description_E }}</p>
              <p><i class="fa fa-map-marker"></i> {{ evenement.ID_Lieu.Lieu }} Mahamasina</p>

              <button v-if="showSubscribeButton" @click="subscribe" class="btn btn-primary">S'inscrire</button>
            </div>

          </div>
        </div>
      </div>
    </section>
</template>
  
<script>

export default {
  props: ['id'],
  data() {
    return {
      evenement: {},
      countdown: {
        days: 0,
        hours: 0,
        minutes: 0,
        seconds: 0
      },
      showSubscribeButton: false,
    };
  },
  created() {
    this.fetchEvenementDetails();
    this.updateCountdown();
    setInterval(this.updateCountdown, 1000);
  },
  methods: {
    async fetchEvenementDetails() {
      try {
        const response = await fetch(`/api/evenement-detail/${this.id}/`);
        this.evenement = await response.json();
        this.checkLoginStatus();
      } catch (error) {
        console.error('Erreur lors de la récupération des détails de l\'événement:', error);
      }
    },
    updateCountdown() {
      const now = new Date();
      const eventDate = new Date(this.evenement.Date_Debut_E);
      const difference = eventDate.getTime() - now.getTime();
      const limitDate = new Date(this.evenement.Date_Limite_Inscription);

      this.countdown.days = Math.floor(difference / (1000 * 60 * 60 * 24));
      this.countdown.hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      this.countdown.minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
      this.countdown.seconds = Math.floor((difference % (1000 * 60)) / 1000);

      // Vérifier si l'événement n'est pas encore terminé pour afficher le bouton "S'inscrire"
      if (limitDate > now) {
        this.showSubscribeButton = true;
      } else {
        this.showSubscribeButton = false;
      }
    },
    async checkLoginStatus() {
      try {
        const response = await fetch('/api/check_login/');
        if (response.ok) {
          // User is logged in
          const data = await response.json();
          this.isLoggedIn = true;
          this.username = data.username;
        } else {
          // User is not logged in
          this.isLoggedIn = false;
        }
      } catch (error) {
        console.error('Erreur lors de la vérification de la connexion:', error);
      }
    },
  async subscribe() {
    try {
      const response = await fetch(`/api/inscription-evenement/${this.evenement.ID_Evenement}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',  // Assurez-vous que le backend accepte ce type de contenu
          'X-CSRFToken': this.getCookie('csrftoken')
        },
        body: JSON.stringify({})  // Envoyer un corps vide pour les requêtes POST
      });
      if (response.ok) {
        alert('Vous êtes inscrit à cet événement');
      } else {
        const errorData = await response.json();
        console.error('Erreur lors de l\'inscription:', errorData);
        alert('Erreur lors de l\'inscription: ' + errorData.error);
      }
    } catch (error) {
      console.error('Erreur lors de l\'inscription:', error);
      alert('Erreur lors de l\'inscription');
    }
  },
    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },
    getEventImage(imagePath) {
      return imagePath ? `http://127.0.0.1:8000/static${imagePath}` : ''; // Modifier l'URL selon vos besoins
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString('fr-FR', options);
    }
  }
};
</script>

