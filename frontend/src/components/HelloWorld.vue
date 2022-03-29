<template>
  <v-container>
    <h1>СТОЛЫ</h1>
    <br><br>
    <div v-for="table in tables" :key="table.id">
<!---->
      <router-link :to="'/table/' + table.id">Стол №{{ table.id }}</router-link>
    </div>
  </v-container>
</template>

<script>

export default {
  name: 'HelloWorld',
  data() {
    return {
      tables: [],
    }
  },
  beforeMount() {
    this.axios.get('http://127.0.0.1:8000/api/v1/tables/').then(
      (response) => {
        this.tables = response.data
      }
    )
  },
  methods: {},
}
</script>
