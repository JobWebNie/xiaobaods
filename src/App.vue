<template>
  <div id="app" v-if="!userValidor">
    <el-row>
      <el-col  style="background:#1F2D3D;color:#ffffff;position:fixed;height:100%; width:8%;">
        <MyAside ></MyAside>
      </el-col>
      <el-col style="position:fixed;right:0px;top:0px;height:100%;width:92%;overflow:overlay;">
     <keep-alive>
     <router-view></router-view>
     </keep-alive>
      </el-col>
    </el-row>
  </div>
  <div v-else>
    <el-row>
      <el-col>
        <router-view></router-view>
      </el-col>
      <el-col v-if="userValidor">
        <MyFooter></MyFooter>
      </el-col>
    </el-row>
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
    computed: {
      userValidor() {
        if (this.$route.path == "/login/" || this.$route.path == "/register/" || this.$route.path == "/modify/") {
          return true
        }
      }
    }
  }
</script>
<style>
  body,
  html {
    /*将body默认margin设置为0*/
    margin: 0px;
  }

  a {
    /*设置*a标签的样式*/
    color: black;
  }

  .el-tooltip__popper.is-dark span a {
    /*将第3、4列的a的样式*/
    color: #FFF;
  }

  .el-menu-item.is-active {
    /*添加点击侧导航类目样式突出显示*/
    border-right: 6px solid #34C0E3;
    background: #475669;
  }

  .el-table .cell {
    /*将表格的左边距设置为使表格更为紧凑*/
    padding-left: 0px;
    padding-right: 10px;
    word-break: break-word;
  }

  .el-table th>div {
    padding: 0px;
    word-break: break-word;
  }

  .navlist .list-left .Embellish a {
    background-color: #34C0E3;
    color: #FFF;
    display: inline-block;
    width: 50px;
    text-align: center;
    border-radius: 4px;
  }
  /*公共样式*/

  @media screen and (min-width: 1200px) {
    .navlist,
    .title {
      min-width: 1000px;
    }
    .navlist {
      background-color: #E5E9F2;
      height: 40px;
    }
    .title {
      padding: 0px 2vw;
      background: #34C0E3;
      color: #FFF;
    }
    .title .title-left {
      width: 40%;
    }
    .title .title-right {
      width: 60%;
      text-align: right;
    }
    .navlist .list-left {
      min-width: 680px;
      max-width: 700px;
      width: 60%;
    }
    .navlist .list-right {
      width: 40%;
      border: 1px solid #99A9BF;
      height: 36px;
      padding: 2px 0px 0px 2px;
      max-width: 440px;
      min-width: 420px;
    }
    .navlist .el-input {
      min-width: 130px;
      max-width: 150px;
    }
    .navlist .el-input-number {
      overflow: initial;
    }
    .navlist .list-left .Embellish>a {
      line-height: 28px;
    }
  }
  /*以下是992px~1200px样式*/

  @media screen and (min-width:992px) and (max-width:1200px) {
    /*以下是title和下拉列表list样式*/
    .navlist,
    .title {
      min-width: 800px;
    }
    .title {
      font-size: 1em;
      padding: 0px 2vw;
      background: #34C0E3;
      color: #FFF;
      height: 4vw;
    }
    .title>.title-left {
      width: 40%;
    }
    .title>.title-right {
      width: 60%;
      text-align: right;
    }
    .navlist {
      background-color: #E5E9F2;
    }
    .navlist .el-input__inner {
      font-size: 0.8em;
    }
    .navlist .list-left {
      min-width: 550px;
      max-width: 600px;
      width: 55%;
    }
    .navlist .list-right {
      width: 45%;
      border: 1px solid #99A9BF;
      height: 30px;
      padding: 0px 2px;
      max-width: 340px;
      min-width: 300px;
    }
    .navlist .el-input {
      min-width: 100px;
      max-width: 110px;
    }
    .navlist .el-input .el-input__icon {
      width: 25px;
    }
    .list-right .el-button {
      min-width: 30px;
      max-width: 40px;
      padding-top: 4px;
      height: 22px;
    }
    .el-input--small .el-input__inner {
      height: 25px;
      padding: 0px;
    }
    .navlist .list-left .Embellish>a {
      line-height: 22px;
    }
    /*以下是表格样式*/
    .tablelist {
      font-size: 0.9em;
    }
  }
  /*以下是768~992样式*/

  @media screen and (min-width:768px) and (max-width:992px) {
    /*以下是title和下拉列表list样式*/
    .title {
      max-width: 900px;
      min-width: 700px;
    }
    .title {
      font-size: 1em;
      padding: 0px 2vw;
      background: #34C0E3;
      color: #FFF;
      height: 4vw;
    }
    .title>.title-left {
      width: 40%;
    }
    .title>.title-right {

      width: 60%;
      text-align: right;
    }
    p {
      text-overflow: clip;
      overflow: hidden;
      white-space: nowrap;
    }
    .navlist {
      flex-direction: column;
      background-color: #E5E9F2;
    }
    .list-right {
      height: 30px;
      padding: 0px 2px;
    }
    .navlist .el-input {
      width: 20vw;
    }
    .navlist .el-date-editor.el-input {
      width: 20vw;
    }
    .navlist .list-left .Embellish>a {
      line-height: 25px;
    }
    .tablelist {
      font-size: 0.9em;
    }
  }

</style>
