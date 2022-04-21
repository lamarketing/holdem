<template>
  <div id="container">
    <strong>{{ name }}</strong>
    <p>Произошли изменения.</p>
    <p>
      <ion-button @click="router.go(0)" class="">
        ОБНОВИТЬ ПРИНУДИТЕЛЬНО
      </ion-button>
    </p>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {IonButton} from "@ionic/vue";
import {useRouter} from 'vue-router';

export default defineComponent({
  name: 'ExploreContainer',
  props: {
    name: String
  },
  components: {
    IonButton
  },
  setup() {
    const router = useRouter();
    return {router};
  },
});
</script>

<style scoped>
#container {
  text-align: center;
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}

#container strong {
  font-size: 20px;
  line-height: 26px;
}

#container p {
  font-size: 16px;
  line-height: 22px;
  color: #8c8c8c;
  margin: 0;
}

#container a {
  text-decoration: none;
}
</style>
