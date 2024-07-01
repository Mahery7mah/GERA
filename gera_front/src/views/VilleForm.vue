<template>
  <form @submit.prevent="submitForm">
    <div>
      <label for="nom">Nom:</label>
      <input type="text" id="nom" v-model="villeData.Nom" required>
    </div>
    <button type="submit">Enregistrer</button>
  </form>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      villeData: {
        Nom: '',
      },
    };
  },
  methods: {
    submitForm() {
      axios.post('/api/villes/create/', this.villeData)
        .then(response => {
          console.log(response.data);
          // Rediriger vers la page de liste des villes ou faire une autre action
        })
        .catch(error => {
          console.error(error);
        });
    },
  },
};

</script>