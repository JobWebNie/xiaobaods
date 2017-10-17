<template>
  <div>
    <el-row>
      <img style="position:fixed;left:36vh;" src="../../assets/Bao-blue.png" alt="">
    </el-row>
    <img style="position:absolute;width:100%;top:10vh;" src="../../assets/login_background.jpg" alt="">
    <el-row style="margin-top:20vh;">
      <el-col style="position:absolute;right:20vw;" :span="4">
        <el-card>
          <div style="padding-bottom:10px;position:relative;">
            <b> 密码登录</b>
          </div>
          <el-form :model="ruleForm" :rules="rules" ref="ruleForm" v-on:submit.prevent="onLogin">
            <el-form-item prop="name">
              <el-input v-model="ruleForm.name"></el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input type="password" v-model="ruleForm.password" @keyup.enter.native="onLogin"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button @click="onLogin" style="background:#FF4949;border:none;width:100%;color:#FFFFFF;">登录</el-button>
            </el-form-item>
            <el-button type="text" @click="onRegister">注册</el-button>
            <el-button type="text" @click="seekPassw">找回密码</el-button>
            <el-button type="text" style="position:absolute;right:20px;" @click="jumpIntoCompare">无用户登录</el-button>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  import {
    mapActions
  } from 'vuex'
  import {
    USER_SIGNIN
  } from '../../store/user'
  export default {
    data() {
      return {
        ruleForm: {
          name: '',
          password: '',
        },
        rules: {
          name: [{
            required: true,
            message: '请输入用户名 ',
            trigger: 'blur'
          }, ],
          password: [{
            required: true,
            message: '请输入密码',
            trigger: 'blur'
          }]
        }
      };
    },
    methods: {
      ...mapActions([USER_SIGNIN]),
      onLogin() {
        this.$refs.ruleForm.validate((valid) => {
          if (valid) {
            var data = JSON.stringify(this.ruleForm)
            this.$http.post('/base/login', {
              data
            }, {
              emulateJSON: true
            }).then((response) => {

              if (response.body.message == "success") {
                this.$message("登陆成功")
                var user = response.body.data

                this.USER_SIGNIN(user)
                var level = this.$store.state.user.level
                setTimeout(() => {
                  if (level < 4) {
                    window.router.push({
                      path: '/illegalword'
                    })
                  } else {
                    window.router.push({
                      path: '/product/hot_product'
                    })
                  }
                }, 1000)
              } else if (response.body.message == "pasErr") {
                this.$message("密码错误")
              } else if (response.body.message == "acountErr") {
                this.$message("用户名错误")
              } else {
                this.$message("服务器不稳定稍后再试")
              }
            })
          } else {
            this.$message('error submit!!');
            return false;
          }
        });
      },
      onRegister() {
        window.router.push({
          path: '/register/'
        })
      },
      seekPassw() {
        window.router.push({
          path: '/modify/'
        })
      },
      jumpIntoCompare() {
        this.USER_SIGNIN({
          id: 'ceshi',
          name: "无名小辈"
        })
        setTimeout(() => {
          window.router.push({
            path: '/illegalword'
          })
        }, 1000)
      }
    }
  }

</script>
