import { createRouter, createWebHistory } from 'vue-router';
import HomeFront from './views/HomeFront.vue'; // Importez la vue HomeFront.vue
import VilleList from './views/VilleList.vue';
import VilleDetail from './views/VilleDetail.vue';
import SelectionUtilisateur from './views/SelectionUtilisateur.vue';
import UtilisateurSimpleForm from './views/UtilisateurSimpleForm.vue';
import PersonnelForm from './views/PersonnelForm.vue';
import ConnexionForm from './views/ConnexionForm.vue';
import DetailEvenement from './views/DetailEvenement.vue';
import DetailArticle from './views/DetailArticle.vue';
import NotificationFront from './views/NotificationFront.vue';
import ArticlePublie from './views/ArticlePublie.vue'; // Import de la nouvelle vue
import EvenementAvenir from './views/EvenementAvenir.vue';
import EvenementTermine from './views/EvenementTermine.vue';


import { decryptId } from './utils'; // Importez la fonction decryptId depuis votre fichier utils.js

const routes = [
  {
    path: '/',
    name: 'HomeFront',
    component: HomeFront,
  },
  {
    path: '/evenement/:encryptedId',
    name: 'EvenementDetail',
    component: DetailEvenement,
    props: (route) => ({ id: decryptId(route.params.encryptedId) }),
  },
  {
    path: '/evenements-avenir',
    name: 'EvenementAvenir',
    component: EvenementAvenir
  },
  {
    path: '/evenements-termines',
    name: 'EvenementTermine',
    component: EvenementTermine
  },
  {
    path: '/article/:encryptedId',
    name: 'ArticleDetail',
    component: DetailArticle,
    props: (route) => ({ id: decryptId(route.params.encryptedId) })
  },
  {
    path: '/articles',
    name: 'ArticlePublie',
    component: ArticlePublie, // Définition de la route pour tous les articles publiés
  },
  {
    path: '/villes',
    name: 'VilleList',
    component: VilleList,
  },
  {
    path: '/villes/:encryptedId',
    name: 'VilleDetail',
    component: VilleDetail,
    props: (route) => ({ id: decryptId(route.params.encryptedId) }), // Décryptez l'ID avant de le passer comme propriété
  },

  {
    path: '/inscription',
    name: 'SelectionUtilisateur',
    component: SelectionUtilisateur,
  },
  {
    path: '/inscription/utilisateur-simple',
    name: 'UtilisateurSimpleForm',
    component: UtilisateurSimpleForm,
  },
  {
    path: '/inscription/personnel',
    name: 'PersonnelForm',
    component: PersonnelForm,
  },  
  {
    path: '/connexion',
    name: 'ConnexionForm',
    component: ConnexionForm,
  },

  {
    path: '/notifications',
    name: 'NotificationFront',
    component: NotificationFront,
  },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;