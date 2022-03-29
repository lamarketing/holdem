import { createStore } from 'vuex'
import table from "@/store/modules/table"

// const debug = process.env.NODE_ENV !== 'production'



export default createStore({
  modules: { table },
})
