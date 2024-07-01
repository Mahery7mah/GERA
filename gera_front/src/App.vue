<template>
  <div id="app">
    <Header />
    <router-view />
    <Footer />
  </div>
</template>

<script>
import Header from './components/HeaderFront.vue';
import Footer from './components/FooterFront.vue';

export default {
  components: {
    Header,
    Footer
  },
  // Comportements
}
</script>

<style lang="scss">
/* Styles Sass pour l'application principale */
</style>