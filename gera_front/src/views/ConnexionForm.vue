<template>
  <section id="contact" class="section-auth section-bg wow fadeInUp" style="visibility: visible; animation-name: fadeInUp;">
    <div class="justify-content-center">

      <div class="container">
        <div class="card">
          <div class="card-body card-connexion">
        <div class="row">
        <div class="col-md-6">
        <div class="section-header">
          <h2>Se connecter</h2>
        </div>
      </div>
        <div class="form">
          <form class="contactForm" @submit.prevent="submitForm">
            <div class="form-row">
              <div class="form-group col-md-6 mb-3">
                <label for="username">Nom d'utilisateur:</label>
                <input v-model="Membre.Nom_Utilisateur_M" type="text" class="form-control" id="username" required>
              </div>

              <div class="form-group col-md-6 mb-3">
                <label for="password">Mot de passe:</label>
                <input v-model="Membre.Mot_De_Passe_M" type="password" class="form-control" id="password" required>
              </div>
            </div>
            <div class="form-group col-md-6 d-flex align-items-center justify-content-between">
                    <div class="form-check mb-3">
                      <label class="form-check-label">
                        <input type="checkbox" class="form-check-input"> Se souvenir de moi </label>
                    </div>
                    <a href="#" class="forgot-pass">Mot de passe oublié?</a>
                  </div>
            <button class="mb-3" type="submit">Se connecter</button>
            <p class="sign-up">Vous n'avez pas encore de Compte?<a href="/inscription"> S'inscrire</a></p>
          </form>
          </div>
          </div>
          </div>
          
        </div>
      </div>
    </div>

  </section>

</template>

<script>
export default {
  data() {
    return {
      Membre: {
        Nom_Utilisateur_M: '',
        Mot_De_Passe_M: '',
      },
      isLoggedIn: false, // Flag to track login status
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await fetch('/api/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': this.getCookie('csrftoken') // Get CSRF token from cookie
          },
          body: new URLSearchParams({
            'Nom_Utilisateur_M': this.Membre.Nom_Utilisateur_M,
            'Mot_De_Passe_M': this.Membre.Mot_De_Passe_M
          })
        });
        if (response.ok) {
          // Login successful, set flag and redirect if needed
          this.isLoggedIn = true;
          this.$router.push('/');
          alert('Connexion réussie.');
        } else {
          // Handle login errors
          const errorData = await response.json();
          console.error('Erreur lors de la connexion:', errorData);
          alert('Vérifiez votre nom d\'utilisateur ou mot de passe.');
        }
      } catch (error) {
        console.error('Erreur lors de la connexion:', error);
      }
    },
    getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    }
  },
  computed: {
    isUserLoggedIn() {
      // Check if user is logged in based on the flag
      return this.isLoggedIn;
    }
  }
};
</script>