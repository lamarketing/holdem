<template>
  <v-container>
    {{ cards }}
    <v-btn @click="ws">нажать</v-btn>
  </v-container>
</template>

<script>

const id = new Date().getTime()

export default {
  name: 'HelloWorld',
  data() {
    return {
      cards: 0,
      socket: new WebSocket("ws://127.0.0.1:8000/ws/")
    }
  },
  beforeMount() {
    this.getCards()
  },
  methods: {
    getCards() {
      const socket = new WebSocket("ws://127.0.0.1:8000/ws/")
      socket.onmessage = (e) => {
        e = JSON.parse(e.data)
        this.cards = e
      }
      socket.onopen = function (e) {
        console.log("=====connect", e);
        socket.send(JSON.stringify({
          action: "retrieve",
          request_id: id,
          pk: '2c'
        }))
      };
      socket.onclose = (e) => console.log('---end', e)
    },
    ws() {
      this.socket.send(JSON.stringify({
          action: "retrieve",
          request_id: id,
          pk: '2c'
        }))
    },
  },
}
</script>
