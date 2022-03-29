const ws = new WebSocket("ws://127.0.0.1:8000/ws/")

const state = () => ({
  table_url: 'ws',
  card: [],
})

const mutations = {
  card: (state, card) => state.card = card
}

const actions = {
  getCard() {
    ws.onopen = (e) => {
      console.log("=====connect", e);
      ws.send(JSON.stringify({
        action: "retrieve",
        request_id: new Date().getTime(),
        pk: '2c'
      }))
    };
  }
}

const getters = {}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}