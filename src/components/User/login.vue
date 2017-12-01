<style scoped>
  .el-header,
  .el-footer {
    color: #333;
    line-height: 60px;
  }

  .el-main {
    position: relative;
    padding: 0px;
    overflow: hidden;
    height: calc(100vh - 200px);
  }

  .el-footer {
    margin-top: 60px;
  }

</style>
<template>
  <div id="User-login">
    <el-container>
      <el-header>
        <img src="../../assets/logo-title.png" style="height:100%;" alt=""> 小宝后台{{user ? user.name : '请登录!'}}
      </el-header>
      <el-main>
        <!-- <img src="../../assets/background-image.jpg" style="height:100%;" alt="显示错误">-->
        
        <el-container>
          
          <el-main>Main</el-main>
          <el-aside width="600px"><commonValidator></commonValidator></el-aside>
        </el-container>
      </el-main>
      <el-footer>
        <commonFooter></commonFooter>
      </el-footer>
    </el-container>
  </div>
</template>
<script>
  import commonFooter from '../common/Footer.vue';
  import commonValidator from '../common/Validator.vue';
  export default {
    components: {
      commonFooter,
      commonValidator
    },
    data() {
      return {
        user: {
          name: 'niesaisai'
        }
      }
    }
  }

</script>
