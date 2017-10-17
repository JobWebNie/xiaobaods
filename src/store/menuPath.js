import Vue from 'vue'
export const MENUURL_INSERT = 'MENUURL_INSERT' //添加路径

export default {
  state: sessionStorage.menu || '/product/hot_product', 
  mutations: {
    MENUURL_INSERT(state, menu) {
     sessionStorage.setItem('menu',menu)
    
    }
  },
  actions: {
    MENUURL_INSERT({
      commit
    }, menu) {
      commit(MENUURL_INSERT, menu)
    }
  }
}
