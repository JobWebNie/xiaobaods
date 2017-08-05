<template>
    <div>
    <el-row>
    <img style="position:fixed;left:36vh;" src="../../assets/Bao-blue.png" alt="">
     </el-row>
     <img style="position:absolute;height:auto;width:100%;top:10vh;" src="../../assets/login_background.jpg" alt="">
        <el-row style="margin-top:20vh;">
            <el-col  :span="4" :push="15">
            <el-card>
            <div style="padding-bottom:10px;position:relative;">
            <b>邀请码</b>
            <a href="/#/login/" style="position:absolute;right:5px;color:#34c0e3;"><small>去登录</small></a>
            </div>
             <el-form :model="user">
             <el-form-item>
             <el-input v-model="user.id" placeholder="请输入邀请码！">
            </el-input>
            </el-form-item>
            <el-form-item>
            <el-input v-model="user.name" placeholder="请输入账号！" @keyup.enter.native="modify"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button @click="modify" style="background:#FF4949;border:none;width:100%;color:#FFFFFF;">找回密码</el-button>
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
    return {
      user: {id:'',name:''}
    }
  },
    methods:{
        modify(){
             var data = this.user
            this.$http.put('/modify/seekPassw',{data},{emulateJSON:true}).then(response=>{
                      if(response.body.message=="success"){
                                this.$message(response.body.data)
                       }
                        else if(response.body.message=="acountErr"){
                              this.$message("请确认你的邀请码和账户名！")
                          }
                       else{
                            this.$message("服务器不稳定稍后再试")

                       }
            })
        }
    }
}
</script>