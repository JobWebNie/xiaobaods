<template>
  <div class="comment-validator">
    <el-card>
      <div class="comment-validator-title">
        <b> 密码登录</b>
      </div>
      <el-form ref="ruleForm">
        <el-form-item prop="name">
          <el-input></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button>登录</el-button>
        </el-form-item>
        <el-button type="text">注册</el-button>
        <el-button type="text">找回密码</el-button>
        <el-button type="text">无用户登录</el-button>
      </el-form>
    </el-card>
  </div>
</template>
<style scoped>
  .comment-validator {
    position: absolute;
    top:20%;
    right:20%;
  }
  @media screen and (max-width: 400px) {
  .comment-validator {
    top:20%;
    right:10%;
  }
}
  .comment-validator-title {
    padding-bottom: 10px;
    position: relative;
  }

</style>
