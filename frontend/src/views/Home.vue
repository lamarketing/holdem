<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Техасский Холдем - фрироллы</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Фриролы по Техасскому Холдему</ion-title>
        </ion-toolbar>
      </ion-header>
      <ion-grid fixed>
        <h3 class="color-grey">Ближайшие турниры:</h3>
        <ion-row>
          <ion-col size="auto" class="color-grey"><small>время по МСК</small></ion-col>
        </ion-row>
        <ion-row
          v-for="tournament in tournaments"
          :key="tournament.id"
        >
          <ion-col size="auto">
            {{ makeDate(tournament.start) }}</ion-col>
          <ion-col>
            <ion-icon :icon="trophy" color="warning" class="ion-padding-start"/>
            {{ tournament.prize }}
          </ion-col>
        </ion-row>
        <br><br>
        <ion-accordion-group>
          <ion-accordion value="req">
            <ion-item slot="header">
              <ion-label class="color-link">Как зарегистрироваться на турнир?</ion-label>
            </ion-item>
            <ion-list slot="content">
              <ion-item>
                <ul>
                  <li>Регистрация на турнир начинается за 11 минут и заканчивается за 2 секунды до старта.</li>
                  <li>Зайдите в этот промежуток времени во вкладку "Турнир" и нажмите "Зарегистрироваться".</li>
                </ul>
              </ion-item>
            </ion-list>
          </ion-accordion>
          <ion-accordion value="free">
            <ion-item slot="header">
              <ion-label class="color-link">Почему это бесплатно?</ion-label>
            </ion-item>
            <ion-list slot="content">
              <ion-item>
                <ol>
                  <li>Это фриролл;</li>
                  <li>Так требует законодательство РФ;</li>
                </ol>
              </ion-item>
            </ion-list>
          </ion-accordion>
          <ion-accordion value="po">
            <ion-item slot="header">
              <ion-label class="color-link">Нужно ли дополнительное ПО?</ion-label>
            </ion-item>
            <ion-list slot="content">
              <ion-item>
                <ul>
                  <li>Нет, игра происходит в браузере во вкладке "Турнир".</li>
                </ul>
              </ion-item>
            </ion-list>
          </ion-accordion>
          <ion-accordion value="prize">
            <ion-item slot="header">
              <ion-label class="color-link">Кто формирует приз?</ion-label>
            </ion-item>
            <ion-list slot="content">
              <ion-item>
                <ul>
                  <li>Рекламодатели формируют приз. Взамен площадка размещает рекламу во время турнира и в его записи.</li>
                  <li>Когда нет рекламодателей - приз формируется из кармана разработчика данной площадки.</li>
                </ul>
              </ion-item>
            </ion-list>
          </ion-accordion>
        </ion-accordion-group>
      </ion-grid>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent,
  IonGrid, IonRow, IonCol,
  IonIcon,
  IonAccordion, IonList, IonItem, IonLabel, IonAccordionGroup
} from '@ionic/vue';

import {trophy} from 'ionicons/icons';

import {getTournaments} from "@/api/tournaments";
import {makeDate} from "@/utils/date";

export default defineComponent({
  name: 'HomeView',
  setup() {
    return {
      trophy,
      makeDate
    }
  },
  components: {
    IonHeader, IonToolbar, IonTitle, IonContent, IonPage,
    IonRow, IonGrid, IonCol,
    IonIcon,
    IonAccordion, IonList, IonItem, IonLabel, IonAccordionGroup
  },
  data() {
    return {
      tournaments: []
    }
  },
  async ionViewWillEnter() {
    this.tournaments = await getTournaments()
  },
  methods: {},
});
</script>

<style scoped>
.color-link {
  color: #1b6d85;
}
.color-grey {
  color: grey;
}
</style>

