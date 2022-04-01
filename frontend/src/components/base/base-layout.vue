<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>{{ title }}</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <ion-grid fixed>
        <slot />
      </ion-grid>
    </ion-content>
  </ion-page>
</template>

<script>

import {
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonGrid
} from '@ionic/vue';

export default {
  name: "BaseLayout",
  props: ['title'],
  components: {
    IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonGrid
  },
}
</script>

<style>

</style>