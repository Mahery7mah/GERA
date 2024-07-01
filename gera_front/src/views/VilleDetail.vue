<template>
  <div v-if="ville">
    <h1>Détails de la Ville</h1>
    <p>Nom: {{ ville.Nom }}</p>
  </div>
</template>

<script>
export default {
  props: {
    id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      ville: null,
    };
  },
  created() {
    this.fetchVilleDetails();
  },
  methods: {
    async fetchVilleDetails() {
      try {
        const response = await fetch(`/api/ville-detail/${this.id}/`);
        if (response.ok) {
          this.ville = await response.json();
        } else {
          console.error('Erreur lors de la récupération des détails de la ville:', response.statusText);
        }
      } catch (error) {
        console.error('Erreur lors de la récupération des détails de la ville:', error);
      }
    },
  },
};
</script>