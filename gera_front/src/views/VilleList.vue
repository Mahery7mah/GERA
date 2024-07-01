<template>
  <div class="container">
    <div>
      <h1>Liste des Villes</h1>
      <ul>
        <li v-for="ville in villes" :key="ville.ID_Ville">
          {{ ville.Nom }}
          <router-link :to="'/villes/' + encryptId(ville.ID_Ville)">Voir détails</router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { encryptId } from '../utils';

export default {
  data() {
    return {
      villes: [],
    };
  },
  created() {
    this.fetchVilles();
  },
  methods: {
    async fetchVilles() {
      try {
        const response = await fetch('/api/ville-list/');
        this.villes = await response.json();
      } catch (error) {
        console.error('Erreur lors de la récupération des villes:', error);
      }
    },
    encryptId(id) {
      return encryptId(id);
    },
  },
};
</script>