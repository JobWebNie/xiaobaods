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
        require(['@/components/user/Login.vue'], resolve)
      }
    },
    {
      path: '/select/',
      name: 'UserTest',
      component: function (resolve) {
        require(['@/components/common/Select.vue'], resolve)
      }
    },
    {
      path: '/product',
      name: 'ProductTrend',
      component: function (resolve) {
        require(['@/components/page/Product.vue'], resolve)
      }
    },
    {
      path: '/world',
      name: 'ProductWorld',
      component: function (resolve) {
        require(['@/components/page/World.vue'], resolve)
      }
    },
    {
      path: '/property',
      name: 'ProductProperty',
      component: function (resolve) {
        require(['@/components/page/Property.vue'], resolve)
      }
    },
    {
      path: '/property-deal',
      name: 'ProductPropertyDeal',
      component: function (resolve) {
        require(['@/components/page/PropertyDeal.vue'], resolve)
      }
    },
    {
      path: '/weekport',
      name: 'WeekportTrend',
      component: function (resolve) {
        require(['@/components/page/Weekport.vue'], resolve)
      }
    },
    {
      path: '/tool-box',
      name: 'ToolBox',
      component: function (resolve) {
        require(['@/components/page/ToolBox.vue'], resolve)
      }
    },
    {
      path: '*',
      name: '404Page',
      component: function (resolve) {
        require(['@/components/404page.vue'], resolve)
      }
    }
  ]
})
