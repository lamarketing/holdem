<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Турнир</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true" class="page">
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
            <ion-item>
              <ion-avatar></ion-avatar>
              <ion-label>Количество регистраций:
                <ion-icon :icon="people" color="medium" class=""/>
                {{ count_players }}
              </ion-label>
            </ion-item>
          </ion-list>
          <br><br>
          <div v-if="tournament.is_registration">
            <ion-button v-if="!is_registered" color="success" @click="registrate">
              Зарегистрироваться
            </ion-button>
            <ion-button v-else color="danger" @click="unregistrate">
              Отменить регистрацию
            </ion-button>
          </div>
          <div v-else>
            <ion-button disabled="">
              Зарегистрироваться
            </ion-button>
          </div>
          <br>
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
  IonList, IonAvatar, IonIcon,
} from '@ionic/vue';

import {trophy, radioButtonOn, timer, people} from 'ionicons/icons';

import {makeDate} from "@/utils/date";

import {getTokenL, isAuth} from "@/api/auth";

export default defineComponent({
  name: 'TournamentView',
  setup() {
    const customFormatter = (value: number) => `${value}`;
    return {
      trophy, radioButtonOn, timer, people,
      makeDate,
      customFormatter
    }
  },
  components: {
    IonHeader, IonToolbar, IonTitle, IonContent, IonPage,
    IonGrid, IonItem, IonInput, IonLabel, IonButton, IonChip,
    IonList, IonAvatar, IonIcon,
  },
  data() {
    return {
      isLogin: false,
      username: '',
      password: '',
      error_auth: '',
      socket: this.WS(),
      tournament: null,
      count_players: 0,
      is_registered: false,
    }
  },
  ionViewWillEnter() {
    this.isLogin = !!getTokenL()
    this.ON()

  },
  ionViewWillLeave() {
    console.log('Will Leave')
    this.socket.close()
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
          case 'tournament_info':
            this.tournament = mess.tournament[0]
            this.count_players = mess.count_players
            break
          case 'tournament_info_init':
            this.tournament = mess.tournament
            this.count_players = mess.count_players
            break
          case 'registration_open':
            this.tournament = mess.tournament
            this.count_players = 0
            break
          case 'registrate':
            this.is_registered = mess.is_registered
            break
          case 'start_tournament':
          case 'play':
            this.tournament = null
            if (mess.table) {
              this.$router.push({name: 'play'})
            } else {
              this.$router.go(0)
            }
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
    },
  },
});
</script>
<style scoped>
.color-grey {
  color: grey;
}
.page {
  --ion-background-color: darkgreen;
}
</style>
