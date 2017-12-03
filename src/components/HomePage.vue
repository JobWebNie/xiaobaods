<template>
  <div class="HomePage">
    <el-menu @select="handleSelect" background-color="#545c64" text-color="#fff" active-text-color="#34c0e3" :default-active="activeIndex"
      mode="horizontal">
      <el-menu-item index="1">类目趋势</el-menu-item>
      <el-menu-item index="2">行业热词榜</el-menu-item>
      <el-menu-item index="3">属性洞察</el-menu-item>
      <el-menu-item index="4">生e经</el-menu-item>
      <el-menu-item index="5">文件夹</el-menu-item>
      <el-menu-item index="6">工具箱</el-menu-item>
    </el-menu>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">类目趋势</el-breadcrumb-item>
      <el-breadcrumb-item>热销产品</el-breadcrumb-item>
    </el-breadcrumb>
    <el-tabs type="card"  v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="热销产品" name="first">
      <el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        prop="date"
        label="日期"
        width="180">
      </el-table-column>
      <el-table-column
        prop="name"
        label="姓名"
        width="180">
      </el-table-column>
      <el-table-column
        prop="address"
        label="地址">
      </el-table-column>
    </el-table>
    </el-tab-pane>
    <el-tab-pane label="热搜产品" name="second">
       <el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        prop="date"
        label="日期"
        width="180">
      </el-table-column>
      <el-table-column
        prop="name"
        label="姓名"
        width="180">
      </el-table-column>
      <el-table-column
        prop="address"
        label="地址">
      </el-table-column>
    </el-table>
    </el-tab-pane>
  </el-tabs>
  </div>
</template>

<script>
  export default {
    name: 'HomePage',
    data() {
      return {
        activeIndex: '1',
        activeName:'first',
         tableData: [{
            date: '2016-05-02',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }, {
            date: '2016-05-04',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1517 弄'
          }, {
            date: '2016-05-01',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1519 弄'
          }, {
            date: '2016-05-03',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1516 弄'
          }]
      }
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClick(){
        
      }
    }
  }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


</style>
