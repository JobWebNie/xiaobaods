<template>
  <div>
    <common-header activeIndex="product"></common-header>
    <commonChin chinTitle="类目趋势" :chinOptions="chinOptions" :chinSelect="chinSelect"></commonChin>
    <el-tabs v-model="activeName" @tab-click="handleClick" type="border-card">
      <el-tab-pane label="热销产品" name="seller">
        <commonTable :tableData="tableData" :tableTitle="tableTitle" :tableExpend="tableExpend"></commonTable>
      </el-tab-pane>
      <el-tab-pane label="热搜产品" name="search">
        <el-table :data="tableData">
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
  import commonChin from '../common/Chin.vue';
  import commonTable from '../common/Table.vue';
  export default {
    components: {
      commonSelect,
      commonHeader,
      commonChin,
      commonTable
    },
    data() {
      return {
        chinSelect:['牛仔裤','热销排名',7],
        chinOptions: [[{
              label: '牛仔裤',
              value: '牛仔裤'
            }, {
              label: '休闲裤',
              value: '休闲裤'
            }, {
              label: '打底裤',
              value: '打底裤'
            }],[{
              value: '热销排名',
              label: '热销排名'
            }, {
              value: '支付转化率指数',
              label: '支付转化率指数'
            }, {
              value: '交易增长幅度',
              label: '交易增长幅度'
            }, {
              value: '支付子订单数',
              label: '支付子订单数'
            }],[{
              value: 7,
              label: '近7天'
            }, {
              value: 14,
              label: '近14天'
            }]
        ],
        tableData: [],
        tableTitle:[],
        tableExpend:'',
        TableTotal:20,
        activeName: 'seller'
      }
    },
    created() {
      this.$http.get('/product').then((response)=>{
        console.log(response)
        var obj = response.data
        var body = [];
        var title = [];
        if (obj) {
          for (let j in obj) {
            for (let k in obj[j]) {
              if (k == 'total') {
                this.TableTotal = obj[j][k]
              } else {
                title.push(k)
              }
            }
            break;
          }
          for (let i in obj) {
            body.push(obj[i])
          }
          this.tableTitle = title
          this.tableData = body
        }
            })
        },
        methods: {
          handleClick(v) {
            console.log(v.name, this.$http)
          }
        }
    }

</script>
