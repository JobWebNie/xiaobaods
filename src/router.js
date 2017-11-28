import Vue from 'vue'
import store from './store'
import VueRouter from 'vue-router'
Vue.use(VueRouter)
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
    path: '/weekReport/',
    component: function (resolve) {
      require(['./components/document/weekport.vue'], resolve)
    }
  },
  {
    path: '/testpress',
    component: function (resolve) {
      require(['./components/tool/testpress.vue'], resolve)
    }
  },
  {
    path: '/prodchart',
    component: function (resolve) {
      require(['./components/tool/prodchart.vue'], resolve)
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
    path: '/illegalword/',
    component: function (resolve) {
      require(['./components/tool/illegalword.vue'], resolve)
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
      require(['./components/screen/download.vue'], resolve)
    }
  },
  {
    path: '/datav/',
    meta: {
      Auth: false
    },
    component: function (resolve) {
      require(['./components/screen/data.vue'], resolve)
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
  routes: routes
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
  } else {
    next()
  }
})
export default router;
