import {createApp} from 'vue'
import App from './App.vue'
import router from './router';


import {IonicVue} from '@ionic/vue';

/* Core CSS required for Ionic components to work properly */
import '@ionic/vue/css/core.css';

/* Basic CSS for apps built with Ionic */
import '@ionic/vue/css/normalize.css';
import '@ionic/vue/css/structure.css';
import '@ionic/vue/css/typography.css';

/* Optional CSS utils that can be commented out */
import '@ionic/vue/css/padding.css';
import '@ionic/vue/css/float-elements.css';
import '@ionic/vue/css/text-alignment.css';
import '@ionic/vue/css/text-transformation.css';
import '@ionic/vue/css/flex-utils.css';
import '@ionic/vue/css/display.css';

import axios from 'axios'
import VueAxios from 'vue-axios'

/* Theme variables */
import './theme/variables.css';
import './theme/core.css';

/* Global components */
import BaseLayout from './components/base/base-layout.vue';


// import { Storage } from '@ionic/storage';
//
// const store = new Storage();

const app = createApp(App)
    .use(IonicVue)
    .use(router)
    .use(VueAxios, axios);
    // .use(store.create);

app.component('base-layout', BaseLayout)

router.isReady().then(() => {
    app.mount('#app');
});