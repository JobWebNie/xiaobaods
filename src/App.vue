<template>
  <div id="app">
    <div v-if="leftSide" class="leftSide">
      <MyAside></MyAside>
    </div>
    <div v-bind:class="[leftSide?toggle:full]">
          <router-view></router-view>  
    </div>
    <div id="footer" v-if="!leftSide">
      <MyFooter></MyFooter>
    </div>
  </div>
</template>
<script>
  import MyAside from './aside.vue'; //侧边
  import MyFooter from './footer.vue'; //底部
  export default {
    components: {
      MyAside,
      MyFooter
    },
    data() {
      return {
        toggle: 'toggle',
        full: 'full'
      }
    },
    computed: {
      leftSide() {
        return this.$route.meta.Auth == undefined
      }
    }
  }

</script>
<style>
  @import './assets/css/index.css';
  /**/

  body {
    /*将body默认margin设置为0*/
    margin: 0px;
  }

  #app {
    height: 100%;
    width: 100%;
    position: absolute;
    overflow: hidden;
  }

  .toggle {
    margin-left: 8vw;
    height: 100vh;
  }

  .leftSide {
    position: fixed;
    left: 0px;
    background: #1F2D3D;
    color: #ffffff;
    width: 8vw;
    height: 100vh;
  }

  .full {
    margin-left: 0vw;
    height: 100vh;
  }

  #footer {
    width: 100%;
    position: absolute;
    bottom: 15px;
    text-align: center;
  }
</style>
