<template>
  <div>
    <el-row class="title" type="flex" justify="space-between" align="middle">
      <el-col class="title-left">
        <h3>计算器</h3>
      </el-col>
    </el-row>
    <el-col :span="4" :push="1">
      <b> 选择：</b>
      <el-radio-group v-model="slename" @change="changename">
        <el-radio label="牛仔裤">牛仔裤</el-radio>
        <el-radio label="打底裤">打底裤</el-radio>
      </el-radio-group>
      <br>
      <b> 输入</b>
      <el-input v-model="input" placeholder="请输入内容"></el-input>
      <div>
        <b>结果：</b>{{result}}</div>
    </el-col>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        slename: '牛仔裤',
        input: 0,
        result: null,
        m: null,
        n: null,
        b: null,

      }
    },
    watch: {
      input: function (val, oldVal) {
        this.result = this.m * val + this.n * val * val + this.b
      }
    },
    mounted() {
      this.changename()
    },
    methods: {
      changename() {

        this.$http.post('conversion/parms', {
          name: this.slename
        }, {
          emulateJSON: true
        }).then((response) => {
          this.m = response.data.coef_0
          this.n = response.data.coef_1
          this.b = response.data.intercept
          this.result = this.m * this.input + this.n * this.input * this.input + this.b
        })
      }

    }
  }

</script>
