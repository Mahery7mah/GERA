<template>
<footer id="footer">
    <div class="footer-top">
      <div class="container">
        <div class="row">
          <div class="col-lg-3 col-md-6 footer-info">
            <div id="logo" class="pull-left">
            <a href="/" class="scrollto"><img src="../assets/images/logo.png" alt="" title=""></a>
            </div>
            <div>
            <p>Gera : Vous pouvez consulter les événements de MESUPRES ici <br>
            @MesuPreS 2009 - 2024 <br>
            Ministère de l'Enseignement Supérieur et de la Recherche Scientifique
            </p>
          </div>
          </div>
          <div class="col-lg-3 col-md-6 footer-links">
            <h4>Liens Utils</h4>
            <ul>
              <li><i class="fa fa-angle-right"></i> <a href="/">Acceuil</a></li>
              <li><i class="fa fa-angle-right"></i> <a @click="scrollToSection('Evenement-A-Venir')">Evenements A venir</a></li>
              <li><i class="fa fa-angle-right"></i> <a @click="scrollToSection('Evenement-Termnine')">Archive des événements</a></li>
              <li><i class="fa fa-angle-right"></i> <a @click="scrollToSection('articles')">Articles</a></li>
            </ul>
          </div>
          <div class="col-lg-3 col-md-6 footer-links">
            <h4>Liens Rapides</h4>
            <ul>
              <li><i class="fa fa-angle-right"></i> <a href="#">Home</a></li>
              <li><i class="fa fa-angle-right"></i> <a href="https://www.mesupres.gov.mg">Site Officiel</a></li>
              <li v-if="!isUserLoggedIn"><i class="fa fa-angle-right"></i> <a href="/inscription">Inscription</a></li>
              <li v-if="!isUserLoggedIn" ><i class="fa fa-angle-right"></i> <a href="/connexion">Connexion</a></li>
            </ul>
          </div>
          <div class="col-lg-3 col-md-6 footer-contact">
            <h4>Contacter-Nous</h4>
            <p>
              Rue Ferdinand kasange, Tsimbazaza<br>
              Antananarivo 101 <br>
              <strong>Tel</strong> +261 <br>
              <strong>Email:</strong> commesupres@gmail.com<br>
            </p>
            <div class="social-links">
              <a href="#" class="twitter"><i class="fab fa-twitter"></i></a>
              <a href="#" class="facebook"><i class="fab fa-facebook"></i></a>
              <a href="#" class="instagram"><i class="fab fa-instagram"></i></a>
              <a href="#" class="google-plus"><i class="fab fa-google-plus"></i></a>
              <a href="#" class="linkedin"><i class="fab fa-linkedin"></i></a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      <div class="copyright">
        &copy;<strong>MesuPreS.2024</strong>
      </div>
    </div>
  </footer><!-- #footer -->
</template>
<script>
export default {
  data() {
    return {
      isLoggedIn: false, // Flag to track login status
      username: '', // Username of logged-in user
      showDropdown: false, // Flag to control dropdown visibility
    };
  },
  methods: {
    async logout() {
      try {
        const response = await fetch('/api/logout/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': this.getCookie('csrftoken') // Get CSRF token from cookie
          }
        });
        if (response.ok) {
          // Logout successful, reset flag and username
          this.isLoggedIn = false;
          this.username = '';
          this.$router.push('/');
          alert('Déconnexion réussie.');
        } else {
          // Handle logout errors
          const errorData = await response.json();
          console.error('Erreur lors de la déconnexion:', errorData);
          alert('Erreur lors de la déconnexion.');
        }
      } catch (error) {
        console.error('Erreur lors de la déconnexion:', error);
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
    getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    },
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    scrollToSection(sectionId) {
      const el = document.getElementById(sectionId);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
    },
  },
  computed: {
    isUserLoggedIn() {
      // Check if user is logged in based on the flag
      return this.isLoggedIn;
    }
  },
  async created() {
    // Check if the user is logged in when the component is created
    await this.checkLoginStatus();
    this.$router.beforeEach(async (to, from, next) => {
      if (to.path === '/' && !this.isLoggedIn) {
        await this.checkLoginStatus();
      }
      next();
    });
  },
};
</script>