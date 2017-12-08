import Vue from 'vue'
export const PRODUCT_SEARCH = 'PRODUCT_SEARCH' //添加路径

export default {
  state:{
    Id:'',
    category:'',
    table:''
  },
  mutations: {
    PRODUCT_SEARCH(state,prod) {
     Vue.set(state,'Id',prod.Id)
     Vue.set(state,'category',prod.category)
     Vue.set(state,'table',prod.table)
    }
  },
  actions: {
    PRODUCT_SEARCH({commit}, prod) {
      commit(PRODUCT_SEARCH, prod)
    }
  }
}
