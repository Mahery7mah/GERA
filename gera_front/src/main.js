import { createApp } from 'vue';

import App from './App.vue';
import router from './router';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

import '@fortawesome/fontawesome-free/css/all.css'
import './assets/styles/theme/image.css'
import './assets/styles/theme/image.css'
import './assets/styles/theme/imagecaption.css'
import './assets/styles/theme/imageinsert.css'
import './assets/styles/theme/imageplaceholder.css'
import './assets/styles/theme/imageresize.css'
import './assets/styles/theme/imagestyle.css'
import './assets/styles/theme/imageuploadicon.css'
import './assets/styles/theme/imageuploadloader.css'
import './assets/styles/theme/textalternativeform.css'
import './assets/styles/styles.css'


import WOW from 'wow.js'; // Import de wow.js



const app = createApp(App);
const wow = new WOW(); // Initialisation de WOW
wow.init();

app.use(router);

app.mount("#app");

