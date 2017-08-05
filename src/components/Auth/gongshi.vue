<template>
  <div>
    <el-row class="title" type="flex" justify="space-between" align="middle">
      <el-col class="title-left">
        <h3>公式：Y=mX1+nX^2+b</h3>
      </el-col>
      <el-col class="title-right">
      </el-col>
    </el-row>
    <el-row class="navlist" type="flex" justify="space-around" align="middle">
      <el-col :span="12">
        <el-input v-model="input" placeholder="请输入内容"></el-input>
      </el-col>
      <div>{{result}}</div>
    </el-row>
  </div>
</template>
<script>
 export default {
  data() {
    return {
      input: 0,
      result:null,
      m:null,
      n:null,
      b:null,
    }
  },
  watch:{
    input:function(val, oldVal){
       this.result=this.m*val+this.n*val*val+this.b
    }
  },
  mounted(){
    this.$http.post('conversion/parms',{name:'打底裤'}, {emulateJSON: true}).then((response)=>{
      this.m= response.data.coef_0
      this.n= response.data.coef_1
      this.b = response.data.intercept
      this.result=this.m*this.input+this.n*this.input*this.input+this.b
    })
  }
}
</script>
