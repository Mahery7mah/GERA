<template>
  <section id="contact" class="section-auth section-bg wow fadeInUp">
    <div class="container">
      <div class="section-header">
        <h2>Notifications</h2>
      </div>
      <button class="btn btn-primary float-end" @click="markAllAsRead">
        <i class="fa fa-check"></i>
      </button>
    </div>
    <div class="container">
      <ul class="list-group">
        <a
          v-for="notification in notifications"
          :key="notification.ID_Notification"
          :href="'/evenement/' + encryptId(notification.ID_Evenement)"
          class="list-group-item"
          style="cursor: pointer;"
        >
          <div class="d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center">
              <div class="notification-image">
                <img :src="notification.evenement_image" alt="Image de l'événement">
              </div>
              <div class="notification-content">
                <strong>{{ notification.evenement_titre }}</strong>
                <p class="message-width">{{ notification.Message }}</p>
              </div>
            </div>
            <div class="notification-details">
              <div class="notification-date">{{ formatDate(notification.Date_Envoi) }}</div>
              <button class="btn btn-link">
                <i class="fa fa-ellipsis-v"></i>
              </button>
            </div>
          </div>
        </a>
      </ul>
    </div>
  </section>
</template>

<script>
import { encryptId } from '../utils';

export default {
  data() {
    return {
      notifications: [],
    };
  },
  methods: {
    async fetchNotifications() {
      try {
        const response = await fetch('/api/notifications/');
        if (response.ok) {
          this.notifications = await response.json();
        } else {
          console.error('Erreur lors de la récupération des notifications.');
        }
      } catch (error) {
        console.error('Erreur lors de la récupération des notifications:', error);
      }
    },
    async markAllAsRead() {
      try {
        const response = await fetch('/api/notifications/mark-all-as-read/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': this.getCookie('csrftoken'), // Get CSRF token from cookie
          },
        });
        if (response.ok) {
          // Mark all notifications as read
          this.notifications.forEach((notification) => {
            notification.Est_Lu = true;
          });
          // Update unread count immediately
          this.$emit('updateUnreadCount', 0);
        } else {
          console.error('Erreur lors du marquage des notifications comme lues.');
        }
      } catch (error) {
        console.error('Erreur lors du marquage des notifications comme lues:', error);
      }
    },
    redirectToEvent(eventId) {
      this.$router.push(`/evenement/${eventId}`);
    },
    getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString();
    },
    encryptId(id) {
      return encryptId(id);
    },
  },
  async created() {
    // Fetch notifications when the component is created
    await this.fetchNotifications();
  },
};
</script>

<style scoped>
/* Styles spécifiques à la page de notifications */
.notification-image img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 15px;
}

.notification-details {
  display: flex;
  align-items: center;
}

.notification-date {
  margin-right: 15px;
}

.message-width{
  width : 500px !important;
}
</style>