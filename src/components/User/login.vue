<style scoped>

  .el-main {
    position: relative;
    top:30px;
    padding: 0px;
    height: calc(100vh - 300px);
    background:url('../../assets/background-image.jpg') no-repeat center;
  }

  .el-footer {
    margin-top: 60px;
  }

  .bg-purple {
    height: calc(100vh - 200px);
  }

</style>
<template>
  <div id="User-login">
    <el-container>
      <el-header>
        <img src="../../assets/logo-title.png" style="height:80px;" alt="">
      </el-header>
      <el-main>
            <commonValidator></commonValidator>
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
