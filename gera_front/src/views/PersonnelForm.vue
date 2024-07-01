<template>
      <section id="contact" class="section-auth section-bg wow fadeInUp" style="visibility: visible; animation-name: fadeInUp;">
        <div class="justify-content-center">

          <div class="container">
            <div class="card">
              <div class="card-body card-inscription-personnel">
            
            <div class="row">
            <div class="col-md-6">
            <div class="section-header">
          <h2>S'incrire en tant que Personnel</h2>
        </div>        
      </div>
      <div class="form">

  <form class="contactForm" @submit.prevent="submitForm">
    <div class="form-row">
      <div class="form-group col-md-6">
    <label>Nom d'utilisateur:</label>
    <input class="form-control" type="text" v-model="Personnel.Nom_Utilisateur_M" required><br>
  </div>
  <div class="form-group col-md-6">

    <label>Mot de passe:</label>
    <input class="form-control" type="password" v-model="Personnel.Mot_De_Passe_M" required><br>
  </div>
  <div class="form-group col-md-6">

    <label>Numéro Matricule:</label>
    <input class="form-control" type="text" v-model="Personnel.Matricule_M" required><br>
  </div>

</div>
    <button type="submit">S'inscrire</button>
    <p class="sign-up mt-2">Avez vous déja un compte?<a href="/connexion"> Se connecter</a></p>

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
      Personnel: {
        Matricule_M: '',
        Nom_Utilisateur_M: '',
        Mot_De_Passe_M: '',
      }
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await fetch('/api/inscription/personnel/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.Personnel)
        });
        if (response.ok) {
          // Mise à jour réussie, rediriger l'utilisateur
          this.$router.push('/connexion');
        } else {
          // Gérer les erreurs de mise à jour
          const errorData = await response.json();
          console.error('Erreur lors de la mise à jour du personnel:', errorData);
        }
      } catch (error) {
        console.error('Erreur lors de la mise à jour du personnel:', error);
      }
    }
  }
};
</script>