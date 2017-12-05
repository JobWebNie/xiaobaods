<template>
  <div>
    <common-header activeIndex="world"></common-header>
     <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">类目趋势</el-breadcrumb-item>
      <el-breadcrumb-item>热销产品</el-breadcrumb-item>
      <el-breadcrumb-item>
        <common-select></common-select>
      </el-breadcrumb-item>
    </el-breadcrumb>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="热销产品" name="seller">
        <el-table :data="tableData" style="width: 100%">
          <el-table-column prop="date" label="日期" width="180">
          </el-table-column>
          <el-table-column prop="name" label="姓名" width="180">
          </el-table-column>
          <el-table-column prop="address" label="地址">
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="热搜产品" name="search">
        <el-table :data="tableData" style="width: 100%">
          <el-table-column prop="date" label="日期" width="180">
          </el-table-column>
          <el-table-column prop="name" label="姓名" width="180">
          </el-table-column>
          <el-table-column prop="address" label="地址">
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
<script>
import commonSelect from '../common/Select.vue';
import commonHeader from '../common/Header.vue';
export default {
    components: {
      commonSelect,
      commonHeader
    },
    data() {
        return {
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
        }],
        activeName: 'seller'
        }
    },
    mounted(){
      
    },
    methods:{
       handleClick(v) {
        console.log(v.name)
      }
    }
}
</script>