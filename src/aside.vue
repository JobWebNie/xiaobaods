<template>
  <div>
    <div class="slide_title">
      <div class="user_name">
        <img src="./assets/BaoTitle.png" alt="">
        <span @click="animation">{{user.name}}<small v-show="userLevel==9" @click="showDatav">大屏数据</small></span>
      </div>
    </div>
    <el-menu v-show="midlevel" :default-active="defaultActive" :router="true" theme="dark">
      <el-submenu index="product">
        <template slot="title">类目趋势</template>
        <el-menu-item index="hot_product" :route="{path:'/product/hot_product/'}">热销商品趋势分析</el-menu-item>
        <el-menu-item index="search_prod" :route="{path:'/product/search_prod/'}">流量商品趋势分析</el-menu-item>
      </el-submenu>
      <el-submenu index="word">
        <template slot="title">行业热词榜</template>
        <el-menu-item v-show="midlevel" index="key_word" :route="{path:'/word/key_word/'}">热搜核心词</el-menu-item>
        <el-menu-item v-show="midlevel" index="up_word" :route="{path:'/word/up_word/'}">飙升核心词</el-menu-item>
        <el-menu-item v-show="lowlevel" index="soare_word" :route="{path:'/word/soare_word'}" class="topkeys">急速飙升词</el-menu-item>
        <el-menu-item v-show="midlevel" index="compare" :route="{path:'/word/compare'}">标记词</el-menu-item>
      </el-submenu>
      <el-submenu v-show="midlevel" index="proper">
        <template slot="title">属性洞察</template>
        <el-menu-item index="detail" :route="{path:'/proper/detail'}">属性详情</el-menu-item>
        <el-menu-item v-show="highlevel" index="gongshi" :route="{path:'/proper/gongshi'}">测试公式</el-menu-item>
      </el-submenu>
      <el-submenu v-show="midlevel" index="trade">
        <template slot="title">生e经</template>
        <el-menu-item index="volume" :route="{path:'/trade/volume/'}">属性成交量分布</el-menu-item>
        <el-menu-item index="grail" :route="{path:'/trade/grail/'}">属性成交趋势</el-menu-item>
        <el-menu-item v-show="false" index="freshdata" :route="{path:'/trade/freshdata/'}">实时数据</el-menu-item>
        <el-menu-item v-show="false" index="course" :route="{path:'/trade/course/'}">lunbo</el-menu-item>
      </el-submenu>
    </el-menu>
  </div>
</template>
<script>
  import {
    mapActions,
    mapState
  } from 'vuex'
  export default {
    data() {
      return {
        userLevel: 4,
        highlevel: false,
        midlevel: false,
        lowlevel: false
      }
    },
    computed: {
      ...mapState({
        user: state => state.user
      }),
      defaultActive() {
        return this.$route.path.split('#')[1]
      }
    },
    created() {
      var level = this.user.level
      switch (level) {
        case 9:
          this.highlevel = this.midlevel = this.lowlevel = true
          break;
        case 4:
          this.midlevel = this.lowlevel = true
          break;
        default:
          this.lowlevel = true
          break;
      }
    },
    methods: {
      animation() {
        this.userLevel = this.user.level
      },
      showDatav() {
        window.router.push({
          path: '/datav/'
        })

          if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen();
          } else if (document.documentElement.msRequestFullscreen) {
            document.documentElement.msRequestFullscreen();
          } else if (document.documentElement.mozRequestFullScreen) {
            document.documentElement.mozRequestFullScreen();
          } else if (document.documentElement.webkitRequestFullscreen) {
            document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
          }
       
      }
    }
  }

</script>
<style>
  .user_name img {
    width: 100%;
  }

  .user_name {
    height: 14vh;
    position: relative;
    background: #1F343D;
  }

  .user_name span {
    position: absolute;
    color: #FFF;
    font-weight: bold;
    bottom: 10%;
    left: 25%;
  }

  .topkeys {
    color: #FFF;
    background-image: url(./assets/Alg_0.1.png);
  }

</style>
