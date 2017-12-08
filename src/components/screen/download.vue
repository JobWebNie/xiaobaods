<template>
  <div style="margin:20px;">
   <h3 @click="goBack"><big>&lt;&nbsp;</big>返回</h3>
    <el-row :gutter="20">
      <el-col :span="4" v-for="(item,key) in pictures">
        <el-card :body-style="{ padding: '0px' }">
         <a :href="item.detail">
          <img :src="item.url" class="image">
         </a>
          <div style="padding: 10px 5px;">
            <div class="clearfix">
              <span style="white-space:nowrap;">{{item.name}}</span>
              <time class="time">订单数 {{item.count}}</time>
            </div>
            <div class="clearfix">
              <el-button type="text" class="button" @click="PICTURE_PUT(key)">删除</el-button>
              <el-button type="text" class="button right" @click="toHref(item.url)">下载</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
 import {download} from '../../assets/js/download'
  import {mapActions} from 'vuex'
  export default {
    data(){
      return{
        pictures:this.$store.state.picture
      }
    },
    methods: {
      ...mapActions(['PICTURE_PUT']),
      toHref(href) {//下载某一张图片
       download(href)
      },
      goBack(){
       history.back()
      }
    }
  }

</script>

<style scoped>
  .time {
    display: inline-block;
    position: absolute;
    right: 0px;
    font-size: 13px;
    color: #999;
  }

  .clearfix {
    position: relative;
    margin-top: 5px;
    line-height: 12px;
  }

  .image {
    width: 100%;
    display: block;
    height: 15vw;
  }

  .button {
    padding-bottom: 0px;
  }

  .right {
    position: absolute;
    right: 0px;
  }

</style>
