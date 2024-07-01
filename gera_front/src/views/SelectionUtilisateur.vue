<template>
  <main>
    <section id="contact" class="section-auth section-bg wow fadeInUp" style="visibility: visible; animation-name: fadeInUp;">
      <div class="container">

        <div class="card card-principal justify-content-center">
                  
        <div class="section-header">
          <h2 class="text-light mt-5">Choisissez le type d'utilisateur</h2>
        </div>
        <div class="row mt-5 mb-5">
    
      <div class="col-sm-6 grid-margin">
        <a class="selection-card" href="/inscription/utilisateur-simple/">
        <div class="card card-simple">
          <div class="card-body">
            <div class="row">
              <div class="col-8 col-sm-12 col-xl-8 my-auto">
                <div class="d-flex d-sm-block d-md-flex align-items-center">
                  <h2 class="mb-0">Utilisateur simple</h2>
                </div>
                <h6 class="text-muted font-weight-normal">S'inscrire en tant qu'Utilisateur Simple</h6>
              </div>
              <div class="icon col-4 col-sm-12 col-xl-4 text-center text-xl-right">
                <i class="icon-lg fa fa-angle-right text-primary ml-auto"></i>
              </div>
            </div>
          </div>
        </div>
      </a>
    
      </div>
      <div class="col-sm-6 grid-margin">
        <a href="/inscription/personnel/">
    
        <div class="card card-personnel">
          <div class="card-body">
            <div class="row">
              <div class="col-8 col-sm-12 col-xl-8 my-auto">
                <div class="d-flex d-sm-block d-md-flex align-items-center">
                  <h2 class="mb-0">Personnel</h2>
                </div>
                <h6 class="text-muted font-weight-normal">S'inscrire en tant que personnel</h6>
              </div>
              <div class="col-4 col-sm-12 col-xl-4 text-center text-xl-right">
                <i class="icon-lg fa fa-angle-right text-danger ml-auto"></i>
              </div>
            </div>
          </div>
        </div>
      </a>
      </div>

    </div>
  </div>
    </div>
    </section>

  </main>

  </template>
  
  <script>
  export default {
    methods: {
      choisirUtilisateurSimple() {
        this.$router.push('/inscription/utilisateur-simple/');
      },
      choisirPersonnel() {
        this.$router.push('/inscription/personnel/');
      }
    }
  }
  </script>