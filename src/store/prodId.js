import Vue from 'vue'
export const PRODUCT_SEARCH = 'PRODUCT_SEARCH' //添加路径

export default {
  state:{
    Id:''
  },
  getters:{
    Id:state => state.Id,
  }, 
  mutations: {
    PRODUCT_SEARCH(state,Id) {
      if(typeof Id == 'string'){
       return state.Id = Id
      }else{
        console.log('不是数字')
      }
    }
  },
  actions: {
    PRODUCT_SEARCH({commit}, Id) {
      commit(PRODUCT_SEARCH, Id)
    }
  }
}
