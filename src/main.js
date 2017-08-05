import Vue from 'vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import store from './store'
import VueResouse from 'vue-resource'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import App from './App.vue'

Vue.use(VueRouter);
Vue.use(VueResouse);
Vue.use(ElementUI);
Vue.filter('number-filter', function (value) {
  // 返回处理后的值
  return parseFloat(value * 100).toFixed(2) + '%'
})
window.Vue = Vue;
const routes = [{
    path: '/product/hot_product/',
    component: function (resolve) {
      require(['./components/Product/hot_product.vue'], resolve)
    }
  },
  {
    path: '/product/search_prod/',
    component: function (resolve) {
      require(['./components/Product/search_prod.vue'], resolve)
    }
  },
  {
    path: '/proper/detail/',
    component: function (resolve) {
      require(['./components/Proper/detail.vue'], resolve)
    }
  },
   {
    path: '/proper/table',
    component: function (resolve) {
      require(['./components/Auth/table.vue'], resolve)
    }
  },
   {
    path: '/proper/gongshi',
    component: function (resolve) {
      require(['./components/Auth/gongshi.vue'], resolve)
    }
  },
  {
    path: '/word/key_word/',
    component: function (resolve) {
      require(['./components/Word/key_word.vue'], resolve)
    }
  },
  {
    path: '/word/up_word/',
    component: function (resolve) {
      require(['./components/Word/up_word.vue'], resolve)
    }
  },
  {
    path: '/word/soare_word/',
    component: function (resolve) {
      require(['./components/Word/soare_word.vue'], resolve)
    }
  },
  {
    path: '/word/compare/',
    component: function (resolve) {
      require(['./components/word/compare.vue'], resolve)
    }
  },
  {
    path: '/trade/volume/',
    component: function (resolve) {
      require(['./components/Trade/volume.vue'], resolve)
    }
  },
  {
    path: '/trade/grail/',
    component: function (resolve) {
      require(['./components/Trade/grail.vue'], resolve)
    }
  },
  {
    path: '/picture/download/',
    component: function (resolve) {
      require(['./components/Hugedata/download.vue'], resolve)
    }
  },
  {
    path: '/modify/',
    meta: {
      Auth: false
    },
    component: function (resolve) {
      require(['./components/Auth/modify.vue'], resolve)
    }
  },
  {
    path: '/register/',
    meta: {
      Auth: false
    },
    component: function (resolve) {
      require(['./components/Auth/register.vue'], resolve)
    }
  },
  {
    path: '/login/',
    meta: {
      Auth: false
    },
    component: function (resolve) {
      require(['./components/Auth/login.vue'], resolve)
    }
  },
  {
    path: '*',
    redirect: '/login/'
  }
];
const router = new VueRouter({
  // mode: 'history',
  base: '/', //默认路径
  routes: routes
  //  （缩写为）routes 相当于 routes: routes
});
window.router = router;
router.beforeEach(({
  meta,
  path
}, from, next) => {
  var {
    Auth = true
  } = meta
  var isLogin = Boolean(store.state.user.id)
  if (Auth && !isLogin && path !== '/login/') {
    return next({
      path: '/login'
    })
  }
  next()
})

// window.store = store
new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App)
});
