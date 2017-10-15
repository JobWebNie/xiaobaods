<template>
  <div>
<el-steps :space="100"  direction="vertical" :active="active" >
  <el-step title="已完成"></el-step>
  <el-step title="进行中"></el-step>
  <el-step title="步骤 3"></el-step>
</el-steps>
<el-button style="margin-top: 12px;" @click="next">下一步</el-button>
</div>
</template>


<script>
  export default {
    data() {
      return {
        active: 0
      };
    },

    methods: {
      next() {
        if (this.active++ > 2) this.active = 0;
      }
    }
  }
</script>

