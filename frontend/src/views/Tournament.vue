<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Турнир</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Турнир</ion-title>
        </ion-toolbar>
      </ion-header>
      <ion-grid fixed>
        <div v-if="!isLogin">
          <h5 class="color-grey"> Чтобы участвовать в турнире, представьтесь, пожалуйста,</h5>
          <br>
          <ion-item>
            <ion-label>Логин:</ion-label>
            <ion-input type="text" v-model="username"></ion-input>
          </ion-item>
          <ion-item>
            <ion-label>Пароль:</ion-label>
            <ion-input type="password" v-model="password"></ion-input>
          </ion-item>
          <ion-chip v-if="error_auth" color="danger">{{ error_auth }}</ion-chip>
          <br>
          <ion-button @click="auth">
            отправить
          </ion-button>
          <br><br>
          <p class="color-grey">
            Если вы еще не зарегистрированы на сайте или забыли логин/пароль,
            то получите его в нашем Телеграм-боте.
          </p>
        </div>
        <div v-if="tournament" class="ion-text-center">
          <h2>{{ makeDate(tournament.start) }}</h2>
          <small>время московское</small>
          <br><br>
          <ion-list>
            <ion-item>
              <ion-avatar></ion-avatar>
              <ion-label>Приз
                <ion-icon :icon="trophy" color="warning" class=""/>
                {{ tournament.prize }}
              </ion-label>
            </ion-item>
            <ion-item>
              <ion-avatar></ion-avatar>
              <ion-label>Начальный стек
                <ion-icon :icon="radioButtonOn" color="success" class=""/>
                {{ tournament.init_stack }} фишек
              </ion-label>
            </ion-item>
            <ion-item>
              <ion-avatar></ion-avatar>
              <ion-label>Время на ход
                <ion-icon :icon="timer" color="primary" class=""/>
                {{ tournament.seconds_to_think }} секунд
              </ion-label>
            </ion-item>
          </ion-list>
          <br><br>
          <ion-button v-if="!is_registered" color="success" @click="registrate">
            Зарегистрироваться
          </ion-button>
          <ion-button v-else color="danger" @click="unregistrate">
            Отменить регистрацию
          </ion-button>
          <br>
          <div v-if="is_active">ТУРНИР НАЧАЛСЯ</div>
        </div>
      </ion-grid>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent,
  IonGrid, IonItem, IonInput, IonLabel, IonButton, IonChip,
  IonList, IonAvatar, IonIcon
} from '@ionic/vue';

import {trophy, radioButtonOn, timer} from 'ionicons/icons';

import {makeDate} from "@/utils/date";

import {getTokenL, isAuth} from "@/api/auth";

export default defineComponent({
  name: 'TournamentView',
  setup() {
    return {
      trophy, radioButtonOn, timer,
      makeDate
    }
  },
  components: {
    IonHeader, IonToolbar, IonTitle, IonContent, IonPage,
    IonGrid, IonItem, IonInput, IonLabel, IonButton, IonChip,
    IonList, IonAvatar, IonIcon
  },
  data() {
    return {
      isLogin: false,
      username: '',
      password: '',
      error_auth: '',
      socket: this.WS(),
      tournament: null,
      is_registered: false,
      is_active: false,
      message: "",
    }
  },
  ionViewWillEnter() {
    this.isLogin = !!getTokenL()
    this.ON()

  },
  methods: {
    async auth() {
      this.isLogin = await isAuth(this.username, this.password)
      if (!this.isLogin) {
        this.error_auth = 'Неправильные логин/пароль!'
      } else {
        this.socket = this.WS()
        this.password = ''
        this.username = ''
        this.ON()
      }
    },
    WS: () => new WebSocket("ws://127.0.0.1:8000/ws/tournament/" + "?token=" + getTokenL()),
    ON() {
      this.socket.onmessage = (e: any) => {
        const mess = JSON.parse(e.data)
        console.log(mess)
        switch (mess.type) {
          case 'sendTournamentInfo':
            this.tournament = mess.data.tournament
            this.is_registered = mess.data.is_registered
            this.is_active = mess.data.tournament.active_now
            break
          case 'c_send_tournament_info':
            this.tournament = mess.data.tournament
            this.is_active = mess.data.tournament.active_now
            break
        }
      }
      this.socket.onclose = () => {
        this.tournament = null
        this.is_registered = false
      }
    },
    SEND(command: string) {
      return this.socket.send(
        JSON.stringify({
          command: command
        })
      )
    },
    registrate() {
      this.SEND('registrate')
    },
    unregistrate() {
      this.SEND('unregistrate')
    }
  },
});
</script>
<style scoped>
/*.color-link {*/
/*  color: #1b6d85;*/
/*}*/
.color-grey {
  color: grey;
}

.text-center {

}
</style>
