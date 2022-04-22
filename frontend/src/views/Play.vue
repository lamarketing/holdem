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
        <ion-grid v-if="game.user" class="play">
          <ion-row>
            <ion-col
              v-for="player in table.players"
              :key="player.user"
              size="2"
            >
              <ion-card
                class="player ion-text-nowrap ion-text-center"
                :color="player.move ? 'dark' : 'light'"
              >
                <ion-card-header>{{ player.position }}</ion-card-header>
                <ion-card-content style="padding: 2px">
                  {{ player.user.slice(0, 7) }}
                </ion-card-content>
              </ion-card>
            </ion-col>
          </ion-row>
          <ion-row>
            <ion-col size="10">
              <ion-card style="margin: 5px 0 0 0">
                <ion-list style="padding: 0; margin: 0">
                  <ion-item
                    v-if="action"
                    style="padding: 0; margin: 0"
                    :color="_makeColorAction(action.name)"
                  >
                    <ion-label v-if="game.user == action.created_by.user">
                      Я:
                    </ion-label>
                    <ion-label v-else>
                      {{ action.created_by.user }}:
                    </ion-label>
                    <ion-label>{{ action.name }}</ion-label>
                    <ion-label slot="end">
                      <strong>{{ action.bet }}</strong>
                    </ion-label>
                  </ion-item>
                  <ion-item v-else style="padding: 0; margin: 0" color="medium">
                    <ion-label slot="start">action:</ion-label>
                  </ion-item>
                </ion-list>
              </ion-card>
            </ion-col>
          </ion-row>
          <ion-row class="ion-text-center">
            <ion-col size="2">
              <ion-card v-if="board[0]" class="ion-padding-vertical hand">
                {{ _translateNominal(board[0].nominal) }}
                <ion-label :color="_makeSuitColor(board[0].suit)">
                  {{ _translateSuit(board[0].suit) }}
                </ion-label>
              </ion-card>
              <ion-card v-else class="ion-padding-vertical board">
                FLOP<br>1
              </ion-card>
            </ion-col>
            <ion-col size="2">
              <ion-card v-if="board[1]" class="ion-padding-vertical hand">
                {{ _translateNominal(board[1].nominal) }}
                <ion-label :color="_makeSuitColor(board[1].suit)">
                  {{ _translateSuit(board[1].suit) }}
                </ion-label>
              </ion-card>
              <ion-card v-else class="ion-padding-vertical board">
                FLOP<br>2
              </ion-card>
            </ion-col>
            <ion-col size="2">
              <ion-card v-if="board[2]" class="ion-padding-vertical hand">
                {{ _translateNominal(board[2].nominal) }}
                <ion-label :color="_makeSuitColor(board[2].suit)">
                  {{ _translateSuit(board[2].suit) }}
                </ion-label>
              </ion-card>
              <ion-card v-else class="ion-padding-vertical board">
                FLOP<br>3
              </ion-card>
            </ion-col>
            <ion-col size="2">
              <ion-card v-if="board[3]" class="ion-padding-vertical hand">
                {{ _translateNominal(board[3].nominal) }}
                <ion-label :color="_makeSuitColor(board[3].suit)">
                  {{ _translateSuit(board[3].suit) }}
                </ion-label>
              </ion-card>
              <ion-card v-else class="ion-padding-vertical board">
                TURN<br>4
              </ion-card>
            </ion-col>
            <ion-col size="2">
              <ion-card v-if="board[4]" class="ion-padding-vertical hand">
                {{ _translateNominal(board[4].nominal) }}
                <ion-label :color="_makeSuitColor(board[4].suit)">
                  {{ _translateSuit(board[4].suit) }}
                </ion-label>
              </ion-card>
              <ion-card v-else class="ion-padding-vertical board">
                RIVER<br>5
              </ion-card>
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
                <ion-label slot="start">BET: {{ table.bet }}</ion-label>
              </ion-list>
            </ion-col>
            <ion-col size="5">
              <ion-list class="board-pot">
                <ion-label slot="start">STACK: {{ game.stack }}</ion-label>
              </ion-list>
            </ion-col>
            <ion-col size="5">
              <ion-list class="board-pot">
                <ion-label slot="start">TO CALL: {{ game.to_call }}</ion-label>
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
              <ion-button
                :disabled="!game.move"
                @click="game.to_call ? call() : check()"
              >
                <span v-if="game.to_call">call</span>
                <span v-else>check</span>
              </ion-button>
              <br><br>
              <ion-button color="danger" :disabled="!game.move">
                fold
              </ion-button>
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
                  :disabled="!game.move"
                  color="warning"
                  style="padding: 0 ; margin: 22px 0 0 0"
                >
                  <ion-label slot="start">{{ table.init_bb }}</ion-label>
                  <ion-label slot="end">{{ endRaise }}</ion-label>
                </ion-range>
              </ion-item>
            </ion-col>
            <ion-col size="10">
              <ion-list>
                <ion-radio-group v-model="bet">
                  <ion-row class="small">
                    <ion-col size="2">
                      <ion-label color="warning">2bb</ion-label>
                      <ion-radio :value="table.init_bb * 2" :disabled="!game.move" color="warning"></ion-radio>
                    </ion-col>
                    <ion-col size="2">
                      <ion-label color="warning">3bb</ion-label>
                      <ion-radio :value="table.init_bb * 3" :disabled="!game.move" color="warning"></ion-radio>
                    </ion-col>
                    <ion-col size="2">
                      <ion-label color="warning">4bb</ion-label>
                      <ion-radio :value="table.init_bb * 4" :disabled="!game.move" color="warning"></ion-radio>
                    </ion-col>
                    <ion-col size="2">
                      <ion-label color="warning">5bb</ion-label>
                      <ion-radio :value="table.init_bb * 5" :disabled="!game.move" color="warning"></ion-radio>
                    </ion-col>
                    <ion-col size="2">
                      <ion-label color="warning">6bb</ion-label>
                      <ion-radio :value="table.init_bb * 6" :disabled="!game.move" color="warning"></ion-radio>
                    </ion-col>
                  </ion-row>
                </ion-radio-group>
              </ion-list>
            </ion-col>
            <ion-col size="4" class="ion-padding-top">
              <ion-button color="success" :disabled="!game.move">
                ALL IN
              </ion-button>
            </ion-col>
            <ion-col size="6" class="ion-padding-top">
              <ion-button color="warning" :disabled="!game.move">
                BET/RAISE
              </ion-button>
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
import { defineComponent } from 'vue';
import {
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent,
  IonGrid, IonItem, IonLabel, IonButton,
  IonList,
  IonRow, IonCol,
  IonCard, IonCardHeader, IonCardContent,
  IonRange, IonRadio, IonRadioGroup
} from '@ionic/vue';

import {trophy, radioButtonOn, timer} from 'ionicons/icons';

import {makeDate} from "@/utils/date";

import {getTokenL} from "@/api/auth";

export default defineComponent({
  name: 'PlayView',
  setup() {
    const customFormatter = (value: number) => `${value}`;
    return {
      trophy, radioButtonOn, timer,
      makeDate,
      customFormatter
    }
  },
  components: {
    IonHeader, IonToolbar, IonTitle, IonContent, IonPage,
    IonGrid, IonItem, IonLabel, IonButton,
    IonList,
    IonRow, IonCol,
    IonCard, IonCardHeader, IonCardContent,
    IonRange, IonRadio, IonRadioGroup
  },
  data() {
    return {
      isLogin: false,
      socket: this.WS(),
      game: {user: '', stack: 0, move: false},
      table: {init_bb: 0, how_many_rows: 1},
      board: [] as any,
      hand: [{}, {}],
      bet: 0 as number,
      action: null as any,
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
  computed: {
    endRaise(): number {
      const next_bb = this.table.init_bb * (this.table.how_many_rows + 1)
      return this.game.stack - next_bb
    },
  },
  methods: {
    WS: () => new WebSocket("ws://127.0.0.1:8000/ws/tournament/play" + "?token=" + getTokenL()),
    ON() {
      this.socket.onmessage = (e: any) => {
        const mess = JSON.parse(e.data)
        console.log('PLAY', mess)
        switch (mess.type) {
          case 'table':
            if (!mess.table) break
            if (!this.game) break
            mess.table.players.splice(
              mess.table.players.findIndex(
                (item: { user: string }) => item.user === this.game.user),
              1
            )
            if (mess.table.flop) {
              for (const card of mess.table.flop) {
                this.board.push(card)
              }
            }
            if (mess.table.turn) {
                this.board.push(mess.table.turn[0])
            }
            if (mess.table.river) {
                this.board.push(mess.table.river[0])
            }
            this.table = mess.table
            break
          case 'game':
            if (!mess.game) break
            this.game = mess.game
            this.hand = mess.game.hand
            break
          case 'action':
            this.action = mess.action
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
        case 'r':
          return String.fromCharCode(9829)
        case 's':
          return String.fromCharCode(9824)
      }
    },
    _makeSuitColor(suit: string) {
      switch (suit) {
        case 'c': case 's':
          return 'primary'
        case 'r': case 'd':
          return 'danger'
      }
    },
    _makeColorAction(action_name: string) {
      switch (action_name) {
        case 'Small Blind': case 'Big Blind':
        case 'Check': case 'Call':
          return 'primary'
        case 'Fold':
          return 'danger'
        case 'Bet': case 'Raise':
          return 'warning'
        case 'All In':
          return 'success'
      }
    },
    _makeColorCardPlayer(move: boolean, username: string) {
      if (move) {
        return 'tertiary'
      }
      if (username === this.action.created_by.user) {
        return 'dark'
      }
    },
    _moveFalse() {
      this.game.move = false
    },
    call() {
      this._moveFalse()
      this.SEND('call')
    },
    check() {
      this._moveFalse()
      this.SEND('check')
    },
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
  /*color: white;*/
}

.board-pot {
  background: var(--ion-background-color);
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


/*.page {*/
/*  --ion-background-color: #013210;*/
/*}*/

</style>
