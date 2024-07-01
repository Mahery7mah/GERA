<template>
      <section id="contact" class="section-auth section-bg wow fadeInUp" style="visibility: visible; animation-name: fadeInUp;">
        <div class="justify-content-center">

          <div class="container">
            <div class="card">
              <div class="card-body card-inscription-simple">
            
            <div class="row">
            <div class="col-md-6">
            <div class="section-header">
          <h2>S'incrire en tant que Utilisateur simple</h2>
        </div>
      </div>

        <div class="form">

  <form class="contactForm" @submit.prevent="submitForm">
    <div class="form-row">
      <div class="form-group col-md-6">

    <label>Nom d'utilisateur:</label>
    <input class="form-control"  type="text" v-model="Membre.Nom_Utilisateur_M" required><br>
  </div>

    <div class="form-group col-md-6">

    <label>Mot de passe:</label>
    <input class="form-control"  type="password" v-model="Membre.Mot_De_Passe_M" required><br>
  </div>

    <div class="form-group col-md-6">

    <label>Nom:</label>
    <input class="form-control" type="text" v-model="Membre.Nom_M" required><br>
  </div>

    <div class="form-group col-md-6">

    <label>Prénom:</label>
    <input class="form-control" type="text" v-model="Membre.Prenom_M" required><br>
  </div>

    <div class="form-group col-md-6">

    <label>Téléphone:</label>
    <input class="form-control" type="text" v-model="Membre.Tel_M" required><br>
  </div>

    <div class="form-group col-md-6">

    <label>Adresse Mail:</label>
    <input class="form-control" type="text" v-model="Membre.Mail_M" required><br>
  </div>
  </div>
    <button type="submit">S'inscrire</button>
    <p class="sign-up">Avez vous déja un compte?<a href="/connexion"> Se connecter</a></p>

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
        Nom_M: '',
        Prenom_M: '',
        Tel_M: '',
        Mail_M: '',
      }
    };
  },
  methods: {
    async submitForm() {
    try {
        const response = await fetch('/api/inscription/membre-simple/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                Nom_Utilisateur_M: this.Membre.Nom_Utilisateur_M,
                Mot_De_Passe_M: this.Membre.Mot_De_Passe_M,
                Nom_M: this.Membre.Nom_M,
                Prenom_M: this.Membre.Prenom_M,
                Tel_M: this.Membre.Tel_M, 
                Mail_M: this.Membre.Mail_M
            })
        });
        if (response.ok) {
            // Inscription réussie, rediriger l'utilisateur
            this.$router.push('/connexion');
            alert('Vous etes inscrit avec succès.');

        } else {
            // Gérer les erreurs de l'inscription
            const errorData = await response.json();
            console.error('Erreur lors de l\'inscription:', errorData);

        }
    } catch (error) {
        console.error('Erreur lors de l\'inscription:', error);
    }
}
  }
};
</script>