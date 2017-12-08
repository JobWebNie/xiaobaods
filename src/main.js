import Vue from 'vue'
import Vuex from 'vuex'
import store from './store'
import VueResouse from 'vue-resource'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import router from './router.js'
import App from './App.vue'

Vue.use(VueResouse)
Vue.use(ElementUI)
window.Vue = Vue;
new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App)
});
