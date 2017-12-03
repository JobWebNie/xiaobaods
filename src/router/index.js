import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/components/HomePage'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/login/',
      name: 'UserLogin',
      component: function (resolve) {
        require(['../components/user/Login.vue'], resolve)
      }
    },
    {
      path: '*',
      name: '404Page',
      component: function (resolve) {
        require(['../components/404page.vue'], resolve)
      }
    }
  ]
})
