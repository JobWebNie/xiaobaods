<template>
  <div>
    <div class="slide_title">
      <img src="./assets/BaoTitle.png" alt="">
      <el-button :plain="true"><span>&nbsp;<i class="el-icon-menu el-icon--left"></i></span>&nbsp;{{user.name}}</el-button>
    </div>
    <el-menu  v-show="midlevel" :default-active="defaultActive" :router="true" theme="dark">
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
        <el-menu-item index="gongshi" :route="{path:'/proper/gongshi'}">测试公式</el-menu-item>
        <el-menu-item index="table" :route="{path:'/proper/table'}">测试表格</el-menu-item>
      </el-submenu>
      <el-submenu v-show="midlevel" index="trade">
        <template slot="title">生e经</template>
        <el-menu-item index="volume" :route="{path:'/trade/volume/'}">属性成交量分布</el-menu-item>
        <el-menu-item index="grail" :route="{path:'/trade/grail/'}">属性成交趋势</el-menu-item>
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
        highlevel:true,
        midlevel:false,
        lowlevel:false
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
      var level =this.user.level
      switch(level){
        case 9:
        this.midlevel=this.lowlevel=true
        break;
        case 4:
        this.midlevel=this.lowlevel=true
        break;
        default:
        this.lowlevel=true
        break;
      }
      // if (this.user.level !== null && this.user.level > 4) {
      //    highlevel=true
      
      // } else {
      //   this.show = false
      // }
    }
  }
</script>
<style>
  .slide_title img,
  .slide_title button {
    width: 100%;
  }
  .slide_title .el-button {
    text-align: left;
    width: 5vw;
    padding: 0vw;
    line-height: 1.5vw;
    background: #1F2D3D;
    font-size: 13px;
    color: #FFF;
    margin: 1.2vw;
    border-radius: 0.75vw;
  }

  .slide_title .el-button span {
    width: 1.5vw;
    height: 1.5vw;
    text-align: center;
    display: inline-block;
    position: relative;
    right: 1px;
    border: 1px solid #fff;
    border-radius: 0.75vw;
  }

  .topkeys {
    color: #FFF;
    background-image: url(./assets/Alg_0.1.png);
  }

</style>
