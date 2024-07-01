<template>
  <header class="custom-header navbar navbar-expand-lg fixed-top header-canvas">
    <div class="container d-fex justify-content-between align-items-center">
      <svg id="Calque_1" data-name="Calque 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2065.85 180.35" class="svg-shape">
<path d="M-1.5,4.5" transform="translate(51.65 34.59)" fill="#0af" stroke="#000" stroke-miterlimit="10"/>
<path d="M-31.5,63.5" transform="translate(51.65 34.59)" fill="#0af" stroke="#000" stroke-miterlimit="10"/>
<path d="M-51.65-34.59l2.57,119.25S175.31,229.92,517.05,72.48c208.67-89.55,781,110.24,1497.14,31.29l-2.78-129.32Z" transform="translate(51.65 34.59)" fill="#0af"/></svg>        
      <a href="/" class="scrollto"><img src="../assets/images/logo.png" alt="" title=""></a>

      <a class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <i class="fa fa-bars text-light"></i>
      </a>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link" href="/">Accueil</a>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Evénements
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><a class="dropdown-item" href="/evenements-avenir">A venir</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="/evenements-termines">Terminés</a></li>
            </ul>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/articles">Articles</a>
          </li>
          <li v-if="isUserLoggedIn" class="nav-item notification-link">
            <router-link to="/notifications" class="nav-link position-relative">
              <i class="fa fa-bell"></i>
              <span v-if="unreadCount > 0" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                {{ unreadCount }}
              </span>
            </router-link>
          </li>
          <li v-if="isUserLoggedIn" class="nav-item dropdown ml-auto" @click="toggleDropdown">
            <a class="nav-link" href="#" role="button">
              <i class="fa fa-user-circle" aria-hidden="true"></i> {{ username }}
            </a>
            <div v-if="showDropdown" class="dropdown-menu dropdown-menu-start">
              <li><a class="dropdown-item" href="#">Bonjour, {{ username }}</a></li>
              <li><a class="dropdown-item" href="#" @click="logout">Déconnexion</a></li>
            </div>
          </li>

          <li v-if="!isUserLoggedIn" class="nav-item">
            <router-link to="/inscription" class="nav-link" v-show="!showDropdown">S'inscrire</router-link>
          </li>
          <li v-if="!isUserLoggedIn" class="nav-item">
            <router-link to="/connexion" class="nav-link" v-show="!showDropdown">Se connecter</router-link>
          </li>
        </ul>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  data() {
    return {
      isLoggedIn: false, // Flag to track login status
      username: '', // Username of logged-in user
      showDropdown: false, // Flag to control dropdown visibility
      unreadCount: 0, // Count of unread notifications
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
          await this.fetchUnreadCount();
        } else {
          // User is not logged in
          this.isLoggedIn = false;
        }
      } catch (error) {
        console.error('Erreur lors de la vérification de la connexion:', error);
      }
    },
    async fetchUnreadCount() {
      try {
        const response = await fetch('/api/notifications/');
        if (response.ok) {
          const notifications = await response.json();
          this.unreadCount = notifications.filter(n => !n.Est_Lu).length;
        }
      } catch (error) {
        console.error('Erreur lors de la récupération des notifications:', error);
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
      await this.checkLoginStatus();
      next();
    });
  },
};
</script>

<style>

.custom-header {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.svg-shape {
  width: 100%;
  height: auto;
  position: absolute;
  top: -5px;
  left: 0;
  z-index: -1;
}

.dropdown-menu {
    display: none;
    position: absolute;
    left: 0;
    top: 100%;
}
.nav-item.dropdown:hover .dropdown-menu {
    display: block;
}

.position-relative {
  position: relative;
}
.position-absolute {
  position: absolute;
}
.translate-middle {
  transform: translate(-50%, -50%);
}
.badge {
  display: inline-block;
  padding: 0.25em 0.4em;
  font-size: 75%;
  font-weight: 700;
  line-height: 1;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
  border-radius: 0.25rem;
}
.badge-pill {
  border-radius: 10rem;
}
.bg-danger {
  background-color: #dc3545 !important;
}

.notification-link{
  margin-right : 15px !important;
  margin-left : 15px !important;
}
</style>