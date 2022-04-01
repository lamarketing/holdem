<template>
  <ion-page>
    <ion-tabs>
      <ion-router-outlet></ion-router-outlet>
      <ion-tab-bar slot="bottom">
        <ion-tab-button tab="home" href="/holdem/home">
          <ion-icon :icon="home" />
          <ion-label>Главная</ion-label>
        </ion-tab-button>
        <ion-tab-button tab="tournament" href="/holdem/tournament">
          <ion-icon :icon="ellipse" />
          <ion-label>Турнир</ion-label>
        </ion-tab-button>
        <ion-tab-button tab="watch" href="/holdem/watch">
          <ion-icon :icon="square" />
          <ion-label>Смотреть игры</ion-label>
        </ion-tab-button>
      </ion-tab-bar>
    </ion-tabs>
  </ion-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { IonTabBar, IonTabButton, IonTabs, IonLabel, IonIcon, IonPage, IonRouterOutlet } from '@ionic/vue';
import { ellipse, square, triangle, home } from 'ionicons/icons';

export default defineComponent({
  name: 'MenuView',
  components: { IonLabel, IonTabs, IonTabBar, IonTabButton, IonIcon, IonPage, IonRouterOutlet },
  setup() {
    return {
      ellipse, square, triangle, home
    }
  }
});
</script>
