<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Стол</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true" class="page">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Турнир</ion-title>
        </ion-toolbar>
      </ion-header>
      <ion-grid fixed>
        <ion-grid v-if="game" class="play">
          <ion-row>
            <ion-col
              v-for="player in table.players"
              :key="player.user"
              size="2"
            >
              <ion-card class="player ion-text-nowrap ion-text-center">
                <ion-card-header>
                  <ion-icon :icon="people" color="warning" class=""/>
                </ion-card-header>
                <ion-card-content style="padding: 2px">{{ player.user.slice(0, 7) }}</ion-card-content>
              </ion-card>
            </ion-col>
          </ion-row>
          <ion-row>
            <ion-col size="10">
              <ion-card style="margin: 5px 0 0 0">
                <ion-list style="padding: 0; margin: 0">
                  <ion-item style="padding: 0; margin: 0" color="medium">
                    <ion-label slot="start">action:</ion-label>
                  </ion-item>
                </ion-list>
              </ion-card>
            </ion-col>
          </ion-row>
          <ion-row class="ion-text-center">
            <ion-col size="2">
              <ion-card class="ion-padding-vertical board">
                FLOP<br>1
              </ion-card>
            </ion-col>
            <ion-col size="2">
              <ion-card class="ion-padding-vertical board">FLOP<br>2</ion-card>
            </ion-col>
            <ion-col size="2">
              <ion-card class="ion-padding-vertical board">FLOP<br>3</ion-card>
            </ion-col>
            <ion-col size="2">
              <ion-card class="ion-padding-vertical board">TURN<br>4</ion-card>
            </ion-col>
            <ion-col size="2">
              <ion-card class="ion-padding-vertical board">RIVER<br>5</ion-card>
            </ion-col>
          </ion-row>
          <ion-row class="ion-padding-horizontal">
            <ion-col size="5">
              <ion-list class="board-pot">
                <ion-label slot="start">POT: {{ table.pot }}</ion-label>
              </ion-list>
            </ion-col>
            <ion-col size="5">
              <ion-list class="board-pot">
                <ion-label slot="start">BET:</ion-label>
              </ion-list>
            </ion-col>
            <ion-col size="5">
              <ion-list class="board-pot">
                <ion-label slot="start">STACK: {{ game.stack }}</ion-label>
              </ion-list>
            </ion-col>
            <ion-col size="5">
              <ion-list class="board-pot">
                <ion-label slot="start">TO CALL:</ion-label>
              </ion-list>
            </ion-col>
          </ion-row>
          <ion-row class="ion-text-center">
            <ion-col size="2">
              <ion-card class="ion-padding-vertical hand">
                <ion-label>{{ _translateNominal(hand[0].nominal) }}</ion-label>
                <br>
                <ion-label :color="_makeSuitColor(hand[0].suit)">{{ _translateSuit(hand[0].suit) }}</ion-label>
              </ion-card>
            </ion-col>
            <ion-col size="2">
              <ion-card class="ion-padding-vertical hand">
                <ion-label>{{ _translateNominal(hand[1].nominal) }}</ion-label>
                <br>
                <ion-label :color="_makeSuitColor(hand[1].suit)">{{ _translateSuit(hand[1].suit) }}</ion-label>
              </ion-card>
            </ion-col>
            <ion-col size="6" class="ion-padding-top">
              <ion-button>check/call</ion-button>
              <br><br>
              <ion-button color="danger">fold</ion-button>
            </ion-col>
            <ion-col size="10">
              <ion-item>
                <ion-range
                  v-model="bet"
                  :min="table.init_bb"
                  :max="game.stack"
                  :pin-formatter="customFormatter"
                  pin
                  snaps
                  step="5"
                  color="warning"
                  style="padding: 0 ; margin: 22px 0 0 0"
                >
                  <ion-label slot="start">{{ table.init_bb }}</ion-label>
                  <ion-label slot="end">{{ game.stack - table.init_bb}}</ion-label>
                </ion-range>
              </ion-item>
            </ion-col>
            <ion-col size="10">
              <ion-list>
                <ion-radio-group v-model="bet">
                  <ion-row class="small">
                    <ion-col size="2">
                      <ion-label color="warning">2bb</ion-label>
                      <ion-radio :value="table.init_bb * 2" color="warning"></ion-radio>
                    </ion-col>
                    <ion-col size="2">
                      <ion-label color="warning">3bb</ion-label>
                      <ion-radio :value="table.init_bb * 3" color="warning"></ion-radio>
                    </ion-col>
                    <ion-col size="2">
                      <ion-label color="warning">4bb</ion-label>
                      <ion-radio :value="table.init_bb * 4" color="warning"></ion-radio>
                    </ion-col>
                    <ion-col size="2">
                      <ion-label color="warning">5bb</ion-label>
                      <ion-radio :value="table.init_bb * 5" color="warning"></ion-radio>
                    </ion-col>
                    <ion-col size="2">
                      <ion-label color="warning">6bb</ion-label>
                      <ion-radio :value="table.init_bb * 6" color="warning"></ion-radio>
                    </ion-col>
                  </ion-row>
                </ion-radio-group>
              </ion-list>
            </ion-col>
            <ion-col size="4" class="ion-padding-top">
              <ion-button color="success">ALL IN</ion-button>
            </ion-col>
            <ion-col size="6" class="ion-padding-top">
              <ion-button color="warning">BET/RAISE</ion-button>
            </ion-col>
          </ion-row>
          <br><br>
          <ion-row>
            <ion-col size="10" class="color-grey">
              <ion-label slot="start">dd</ion-label>
              ушел на перерыв
            </ion-col>
          </ion-row>
        </ion-grid>
      </ion-grid>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent,
  IonGrid, IonItem, IonLabel, IonButton,
  IonList, IonIcon,
  IonRow, IonCol,
  IonCard, IonCardHeader, IonCardContent,
  IonRange, IonRadio, IonRadioGroup
} from '@ionic/vue';

import {trophy, radioButtonOn, timer, people} from 'ionicons/icons';

import {makeDate} from "@/utils/date";

import {getTokenL} from "@/api/auth";

export default defineComponent({
  name: 'PlayView',
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
    IonGrid, IonItem, IonLabel, IonButton,
    IonList, IonIcon,
    IonRow, IonCol,
    IonCard, IonCardHeader, IonCardContent,
    IonRange, IonRadio, IonRadioGroup
  },
  data() {
    return {
      isLogin: false,
      socket: this.WS(),
      game: null,
      table: [] as [],
      board: [{}, {}, {}, {}, {}],
      hand: [{}, {}],
      bet: 0 as number,
    }
  },
  ionViewWillEnter() {
    if (getTokenL()) {
      this.isLogin = !!getTokenL()
      this.ON()
    } else {
      this.$router.push({name: 'tournament'})
    }
  },
  methods: {
    WS: () => new WebSocket("ws://127.0.0.1:8000/ws/tournament/play" + "?token=" + getTokenL()),
    ON() {
      this.socket.onmessage = (e: any) => {
        const mess = JSON.parse(e.data)
        console.log('PLAY', mess)
        switch (mess.type) {
          case 'init_game':
            this.game = mess.game
            break
          case 'game_table':
            if (!mess.game) break
            this.game = mess.game
            mess.table.players.splice(
              mess.table.players.findIndex(
                (item: { user: string }) => item.user === mess.game.user),
              1
            )
            this.table = mess.table
            this.hand = mess.game.hand
            break

        }
      }
      this.socket.onclose = () => {
        this.$router.push({name: 'tournament'})
      }
    },
    SEND(command: string) {
      return this.socket.send(
        JSON.stringify({
          command: command
        })
      )
    },
    _translateNominal(nominal: number) {
      if (nominal < 11) return nominal
      switch (nominal) {
        case 11:
          return 'J'
        case 12:
          return 'Q'
        case 13:
          return 'K'
        case 14:
          return 'A'

      }
    },
    _translateSuit(suit: string) {
      switch (suit) {
        case 'c':
          return String.fromCharCode(9827)
        case 'd':
          return String.fromCharCode(9830)
        case 'h':
          return String.fromCharCode(9829)
        case 's':
          return String.fromCharCode(9824)
      }
    },
    _makeSuitColor(suit: string) {
      switch (suit) {
        case 'c': case 's':
          return 'primary'
        case 'h': case 'd':
          return 'danger'
      }
    }
  },
});
</script>
<style scoped>
.color-grey {
  color: grey;
}

.board {
  margin-left: 2px;
  margin-right: 2px;
  padding-top: 15%;
  padding-bottom: 15%;
  background: darkgreen;
}

.card {
  margin-left: 2px;
  margin-right: 2px;
  padding-top: 15%;
  padding-bottom: 15%;
}

.hand {
  margin-left: 2px;
  margin-right: 2px;
  padding-top: 15%;
  padding-bottom: 15%;
  font-size: 35px;
  color: white;
}

.board-pot {
  background: darkgreen;
}

.play {
  --ion-grid-columns: 10;
  --ion-grid-column-padding: 0;
}

.player {
  padding: 2px;
  margin: 2px;
  --ion-background-color: var(--ion-color-light);
}

.action {
  padding: 0;
  margin: 2px;
  background: grey;
}


.page {
  --ion-background-color: darkgreen;
}

</style>
