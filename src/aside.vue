<template>
  <div>
    <div class="slide_title">
      <div class="user_name">
        <img src="./assets/BaoTitle.png" alt="">
        <div style="height:45px;overflow:hidden;margin:20px 54px;">
        <div style="height:20px; width:20px;margin-left: 10px;border-radius: 50%;border:2px solid #fff;"
         @click="showDatav"></div>
        <div style="height:40px;width:40px;border-radius: 50%; border:2px solid #fff;"></div>
        </div>
        <div @click="animation" style="text-align:center;">{{user.name}}</div>
      </div>
    </div>
    
    <el-menu  :default-active="defaultActive" :router="true" theme="dark" @select="handleSelect">
      <el-submenu  v-show="midlevel" index="product">
        <template slot="title">类目趋势</template>
        <el-menu-item index="/product/hot_product" :route="{path:'/product/hot_product'}">热销商品趋势分析</el-menu-item>
        <el-menu-item index="/product/search_prod" :route="{path:'/product/search_prod'}">流量商品趋势分析</el-menu-item>
      </el-submenu>
      <el-submenu v-show="midlevel" index="word">
        <template slot="title">行业热词榜</template>
        <el-menu-item  index="/word/key_word" :route="{path:'/word/key_word'}">热搜核心词</el-menu-item>
        <el-menu-item index="/word/up_word" :route="{path:'/word/up_word'}">飙升核心词</el-menu-item>
        <el-menu-item  index="/word/soare_word" :route="{path:'/word/soare_word'}" class="topkeys">急速飙升词</el-menu-item>
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
      <el-submenu v-show="midlevel" index="document">
        <template slot="title">文件夹</template>
        <el-menu-item  index="/weekReport" :route="{path:'/weekReport'}">周报</el-menu-item>
      </el-submenu>
      <el-submenu index="tool">
        <template slot="title">工具箱</template>
         <el-menu-item  index="/illegalword" :route="{path:'/illegalword'}">标记词</el-menu-item>
        <el-menu-item  index="/testpress" :route="{path:'/testpress'}">测试公式</el-menu-item>
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
        if(this.user.level==9){
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
        }else{
          this.$message('你看不到我')
        }
      },
      handleSelect(value) {
        this.MENUURL_INSERT(value)

      }
    }
  }

</script>
<style>


  .user_name {
    height: 200px;
    background: #1F343D;
  }
  .user_name img {
    width: 100%;
  }

  .topkeys {
    color: #FFF;
    background-image: url(./assets/Alg_0.1.png);
  }

</style>
