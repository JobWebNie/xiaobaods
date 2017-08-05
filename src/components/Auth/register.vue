<template>
<div>
  <el-row>
    <img style="position:fixed;left:36vh;" src="../../assets/Bao-blue.png" alt="">
     </el-row>
  <img style="position:absolute;width:100%;top:10vh;" src="../../assets/login_background.jpg" alt="">
  <el-row style="margin-top:20vh">
    <el-col :span="4"
            :push="15">
            <el-card>
      <div style="padding-bottom:10px;position:relative;">
        <b>用户注册</b>
        <a href="/#/login/" style="position:absolute;right:5px;color:#34c0e3;"><small>去登录</small></a>
      </div>
        <el-form :model="User"
                 :rules="rules2"
                 ref="User"
                 class="demo-ruleForm">
            <el-form-item prop="id">
            <el-input type="string" placeholder="请输入邀请码"
                      v-model="User.id" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item  prop="name">
            <el-input type="string" placeholder="账号"
                      v-model.number="User.name"></el-input>
          </el-form-item>
          <el-form-item  prop="password">
            <el-input type="password" placeholder="密码"
                      v-model="User.password" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item prop="checkPassword">
            <el-input type="password" placeholder="确认密码" v-model="User.checkPassword" auto-complete="off" @keyup.enter.native="submitForm('User')"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="danger" style="width:45%;margin-right:5%" @click="submitForm('User')">提交</el-button>
              <a href="/#/login/"><el-button  type="danger" style="width:45%;">去登录</el-button> </a>
          </el-form-item>
        </el-form>
        </el-card>
    </el-col>
  </el-row>
  </div>
</template>
<script>
export default {
  data() {
    var checkAge = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('账号不能为空'));
      }
      setTimeout(() => {
        if (value.length == undefined) {
          callback(new Error('首字母不能为数字'));
        } else {
          if (value.length < 2 || value.length > 5) {
            callback(new Error('要求2-5个字符'));
          } else {
            callback();
          }
        }
      }, 1000);
    };
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else if (value.length < 6 || value.length > 12) {
        callback(new Error('密码长度6-12'));
      }
      else {
        if (this.User.checkPassword !== '') {
          this.$refs.User.validateField('checkPassword');
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.User.password) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    var id = (rule, value, callback) => {
if(value === ''){
  callback(new Error('如你还没有或者忘记邀请码！请与数据管理员联系。'));
}else {
        callback();
      }
    };
    return {
      User: {
        name: '',
        password: '',
        checkPassword: '',
        id: ''
      },
      rules2: {
        name: [
          { validator: checkAge, trigger: 'blur' }
        ],
        password: [
          { validator: validatePass, trigger: 'blur' }
        ],
        checkPassword: [
          { validator: validatePass2, trigger: 'blur' }
        ],
        id: [
          { validator: id, trigger: 'blur' }
        ]
      }
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          var data = JSON.stringify(this.User)
          this.$http.post('/user/register', { data }, { emulateJSON: true }).then((response) => {

            if (response.body.message == "success") {
              this.$message("注册成功")
              setTimeout(() => {
                window.router.push({ path: '/login/' })
              }, 1000)
            }
            else if (response.body.message == "false") {
              this.$message("注册失败")
            }
            else if (response.body.message == "idErr"){
              this.$message("邀请码错误")
            }
          })

        } else {
          alert('无法提交!!');
          return false;
        }
      });
    }
  }
}
</script>
<style lang="css" scoped>
  .el-row{
    position:relative;
}
.el-card__body{
    background: #FFFFFF;
}
.el-input__inner{
    border-radius: 0px;
    border: 1px solid #DDDDDD;
}
.el-input__inner:focus{
     box-shadow:0px 0px 2px blue;
}
</style>