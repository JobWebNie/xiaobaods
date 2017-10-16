<template>
  <div>
    <div class="slide_title">
      <div class="user_name">
        <img src="./assets/BaoTitle.png" alt="">
        <span @click="animation">{{user.name}}<small v-show="userLevel==9" @click="showDatav">大屏数据</small></span>
      </div>
    </div>
    <el-menu v-show="midlevel" :default-active="defaultActive" :router="true" theme="dark" @select="handleSelect">
      <el-submenu index="product">
        <template slot="title">类目趋势</template>
        <el-menu-item index="/product/hot_product" :route="{path:'/product/hot_product'}">热销商品趋势分析</el-menu-item>
        <el-menu-item index="/product/search_prod" :route="{path:'/product/search_prod'}">流量商品趋势分析</el-menu-item>
      </el-submenu>
      <el-submenu index="word">
        <template slot="title">行业热词榜</template>
        <el-menu-item v-show="midlevel" index="/word/key_word" :route="{path:'/word/key_word'}">热搜核心词</el-menu-item>
        <el-menu-item v-show="midlevel" index="/word/up_word" :route="{path:'/word/up_word'}">飙升核心词</el-menu-item>
        <el-menu-item v-show="midlevel" index="/word/soare_word" :route="{path:'/word/soare_word'}" class="topkeys">急速飙升词</el-menu-item>
      </el-submenu>
      <el-submenu v-show="midlevel" index="proper">
        <template slot="title">属性洞察</template>
        <el-menu-item index="/proper/detail" :route="{path:'/proper/detail'}">属性详情</el-menu-item>
      </el-submenu>
      <el-submenu v-show="midlevel" index="trade">
        <template slot="title">生e经</template>
        <el-menu-item index="/trade/volume" :route="{path:'/trade/volume'}">属性成交量分布</el-menu-item>
        <el-menu-item index="/trade/grail" :route="{path:'/trade/grail'}">属性成交趋势</el-menu-item>
      </el-submenu>
      <el-submenu index="document">
        <template slot="title">文件夹</template>
        <el-menu-item v-show="highlevel" index="/weekReport" :route="{path:'/weekReport'}">周报</el-menu-item>
      </el-submenu>
      <el-submenu index="tool">
        <template slot="title">工具箱</template>
        <el-menu-item v-show="lowlevel" index="/illegalword" :route="{path:'/illegalword'}">标记词</el-menu-item>
        <el-menu-item v-show="highlevel" index="/testpress" :route="{path:'/testpress'}">测试公式</el-menu-item>
      </el-submenu>
    </el-menu>
  </div>
</template>
<script>
  import {
    mapActions,
    mapState
  } from 'vuex'
  import {
    MENUURL_INSERT
  } from './store/menuPath'
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
        user: state => state.user,
        defaultActive: state => state.menu
      }),
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
      ...mapActions([MENUURL_INSERT]),
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

      },
      handleSelect(value) {
        this.MENUURL_INSERT(value)

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
