import Vue from 'vue'
export const PRODUCTID_SEARCH = 'PRODUCTID_SEARCH' //添加路径

export default {
  state: sessionStorage.prodId || '', 
  mutations: {
    PRODUCTID_SEARCH(state,prodId) {
     sessionStorage.setItem('prodId',prodId)
    }
  },
  actions: {
    PRODUCTID_SEARCH({
      commit
    }, prodId) {
      commit(PRODUCTID_SEARCH, prodId)
    }
  }
}
