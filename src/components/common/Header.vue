<template>
  <div class="comment-header">
    <el-menu  background-color="#545c64" text-color="#fff" active-text-color="#34c0e3" mode="horizontal"
             :default-active="activeIndex" :router="true" @select="handleSelect">
      <el-menu-item index="/">首页</el-menu-item>
      <el-menu-item index="product">类目趋势</el-menu-item>
      <el-menu-item index="world">行业热词榜</el-menu-item>
      <el-menu-item index="property">属性洞察</el-menu-item>
      <el-menu-item index="property-deal">生e经</el-menu-item>
      <el-menu-item index="weekport">文件夹</el-menu-item>
      <el-menu-item index="tool-box">工具箱</el-menu-item>
    </el-menu>
  </div>
</template>
<script>
  export default {
    props:{
        activeIndex:{
            type: String,
            default: '/'
        }
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
       
      }
    }
  }

</script>