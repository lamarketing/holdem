<template>
  <v-container>
    <h1>СТОЛ № {{ $route.params['id'] }}</h1>
    <br><br>
    <v-table>
      <tr><td>Users</td><td></td></tr>
      <tr><td>Last Action</td><td></td></tr>
      <tr><td>Modified</td><td></td></tr>
    </v-table>
    <v-row>
      <v-col v-for="c in cards" :key="c">
        <v-btn @click="chooseCard(c.id)">{{ c.id }}</v-btn>
      </v-col>
    </v-row>
    <br><br>
    <v-row>
      <v-col cols="2" class="bg-info">
        Выбранная карта: {{ card }}
      </v-col>
      <v-col cols="5">
        <v-btn @click="makeMotion">ПОХОДИТЬ</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

const id = new Date().getTime()

export default {
  name: 'TableToPlay',
  data() {
    return {
      cards: [],
      card: "2c",
      table: {},
    }
  },
  beforeMount() {
    this.axios.get('http://127.0.0.1:8000/api/v1/cards/').then(
        (response) => this.cards = response.data
    )
    // this.getTable()
  },
  methods: {
    chooseCard(card) {
      this.card = card
    },
    makeMotion(){

    },
    getTable() {
      const socket = new WebSocket("ws://127.0.0.1:8000/ws/table/")
      socket.onmessage = (e) => {
        console.log(JSON.parse(e.data))
      }
      socket.onopen = function (e) {
        console.log("=====connect", e);
        socket.send(JSON.stringify({
          action: "retrieve",
          request_id: id,
          pk: ''
        }))
      };
      socket.onclose = (e) => console.log('---end', e)
    },
  },
}
</script>