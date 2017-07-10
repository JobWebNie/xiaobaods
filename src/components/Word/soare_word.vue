<template>
  <div>
    <el-row class="title" type="flex" justify="space-between" align="middle">
      <el-col class="title-left">
        <h3>急速飙升词</h3>
      </el-col>
      <el-col class="title-right">
        <p>使用机器学习Logistic Regression算法对关键词筛选，提示最具潜力的飙升关键词</p>
      </el-col>
    </el-row>
    <el-row class="navlist" type="flex" justify="space-around" align="middle">
      <el-col :span="12">
        <el-date-picker v-model="value1" :picker-options="pickerOption1" size='small' v-on:change="inputchange"></el-date-picker>
        <el-select v-model="value2" size='small' v-on:change="inputchange">
          <el-option v-for="item in options2" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-cascader v-model="value3" :options="options3" size='small' v-on:change="inputchange"></el-cascader>
        <!--<el-select v-model="value4" size='small' v-on:change="inputchange"><el-option v-for="item in options4" :label="item.label" :value="item.value"></el-option></el-select>-->
        <el-select v-model="value5" size='small' v-on:change="inputchange">
          <el-option v-for="item in options5" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-input-number v-model="value6" size='small' @change="numchange" :step="5" :min="10"></el-input-number>
      </el-col>
      <el-col class="list-right"></el-col>
    </el-row>

    <el-row>
      <el-col>
        <el-table v-loading="loading" :data="Table.tableData_prepag" :height="this.Table.height" style="width: auto">
          <el-table-column :prop="Table.tableData_title[0]" :label="Table.tableData_title[0]" header-align="center" align="center"></el-table-column>
          <el-table-column :prop="Table.tableData_title[1]" :label="Table.tableData_title[1]" header-align="center" align="center"></el-table-column>
          <el-table-column :prop="Table.tableData_title[2]" :label="Table.tableData_title[2]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[3]" :label="Table.tableData_title[3]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[4]" :label="Table.tableData_title[4]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[5]" :label="Table.tableData_title[5]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[6]" :label="Table.tableData_title[6]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[7]" :label="Table.tableData_title[7]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[8]" :label="Table.tableData_title[8]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[9]" :label="Table.tableData_title[9]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[10]" :label="Table.tableData_title[10]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[11]" :label="Table.tableData_title[11]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[12]" :label="Table.tableData_title[12]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[13]" :label="Table.tableData_title[13]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[14]" :label="Table.tableData_title[14]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[15]" :label="Table.tableData_title[15]" header-align="right" align="right"
            v-if="Table.tableData_title[15]"></el-table-column>
          <el-table-column :prop="Table.tableData_title[16]" :label="Table.tableData_title[16]" header-align="right" align="right"
            v-if="Table.tableData_title[16]"></el-table-column>
          <el-table-column :prop="Table.tableData_title[17]" :label="Table.tableData_title[17]" header-align="right" align="right"
            v-if="Table.tableData_title[17]"></el-table-column>
          <el-table-column :prop="Table.tableData_title[18]" :label="Table.tableData_title[18]" header-align="right" align="right"
            v-if="Table.tableData_title[18]"></el-table-column>
          <el-table-column :prop="Table.tableData_title[19]" :label="Table.tableData_title[19]" header-align="right" align="right"
            v-if="Table.tableData_title[19]"></el-table-column>
          <el-table-column :prop="Table.tableData_title[20]" :label="Table.tableData_title[20]" header-align="right" align="right"
            v-if="Table.tableData_title[20]"></el-table-column>
          <el-table-column :prop="Table.tableData_title[21]" :label="Table.tableData_title[21]" header-align="right" align="right"
            v-if="Table.tableData_title[21]"></el-table-column>
        </el-table>
        <div style="position:relative; text-align:center;">
          <el-pagination v-show="Table.overflow" v-bind:size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="Table.PageIndex"
            :page-sizes="[15, 20, 50, 100]" :page-size="Table.prePageCount" layout="total, sizes, prev, pager, next, jumper"
            :total="Table.tableData.length">
          </el-pagination>
        </div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        value1: '',
        pickerOption1: {
          disabledDate(time) {
            var aday = 8.64e7
            var min = new Date('2016-12-12').getTime() - aday
            var max = Date.now() - aday;
            if (time.getTime() > max || time.getTime() < min) {
              return true;
            } else {
              return false;
            }
          }
        },
        value2: '牛仔裤',
        options2: [{
          label: '类目：牛仔裤',
          value: '牛仔裤'
        }, {
          label: '类目：休闲裤',
          value: '休闲裤'
        }, {
          label: '类目：打底裤',
          value: '打底裤'
        }],
        value3: ["热搜核心词", "排名"],
        options3: [{
          value: '热搜核心词',
          label: '热搜核心词',
          children: [{
            value: '排名',
            label: '排名'
          }, {
            value: '搜索人气',
            label: '搜索人气',
          }, {
            value: '相关搜索词数',
            label: '相关搜索词数'
          }, {
            value: '点击率',
            label: '点击率'
          }, {
            value: '点击人气',
            label: '点击人气',
          }, {
            value: '支付转化率',
            label: '支付转化率'
          }, {
            value: '直通车参考价',
            label: '直通车参考价'
          }]
        }, {
          value: '热搜修饰词',
          label: '热搜修饰词',
          children: [{
            value: '排名',
            label: '排名'
          }, {
            value: '搜索人气',
            label: '搜索人气',
          }, {
            value: '相关搜索词数',
            label: '相关搜索词数'
          }, {
            value: '点击率',
            label: '点击率'
          }, {
            value: '点击人气',
            label: '点击人气',
          }, {
            value: '支付转化率',
            label: '支付转化率'
          }, {
            value: '直通车参考价',
            label: '直通车参考价'
          }]
        }, {
          value: '热搜品牌词',
          label: '热搜品牌词',
          children: [{
            value: '排名',
            label: '排名'
          }, {
            value: '搜索人气',
            label: '搜索人气',
          }, {
            value: '相关搜索词数',
            label: '相关搜索词数'
          }, {
            value: '点击率',
            label: '点击率'
          }, {
            value: '点击人气',
            label: '点击人气',
          }, {
            value: '支付转化率',
            label: '支付转化率'
          }, {
            value: '直通车参考价',
            label: '直通车参考价'
          }]
        }, {
          value: '热搜搜索词',
          label: '热搜搜索词',
          children: [{
            value: '排名',
            label: '排名'
          }, {
            value: '搜索人气',
            label: '搜索人气',
          }, {
            value: '商城点击占比',
            label: '商城点击占比'
          }, {
            value: '点击率',
            label: '点击率'
          }, {
            value: '点击人气',
            label: '点击人气',
          }, {
            value: '支付转化率',
            label: '支付转化率'
          }, {
            value: '直通车参考价',
            label: '直通车参考价'
          }]
        }, {
          value: '热搜长尾词',
          label: '热搜长尾词',
          children: [{
            value: '排名',
            label: '排名'
          }, {
            value: '搜索人气',
            label: '搜索人气',
          }, {
            value: '商城点击占比',
            label: '商城点击占比'
          }, {
            value: '点击率',
            label: '点击率'
          }, {
            value: '点击人气',
            label: '点击人气',
          }, {
            value: '支付转化率',
            label: '支付转化率'
          }, {
            value: '直通车参考价',
            label: '直通车参考价'
          }]
        }],
        value5: 7,
        options5: [{
          value: 7,
          label: '显示周期：近7天'
        }, {
          value: 14,
          label: '显示周期：近14天'
        }],
        value6: 10,
        Table: {
          tableData: [],
          tableData_title: [],
          tableData_prepag: [],
          prePageCount: 20,
          PageIndex: 1,
          height: 840,
          overflow: null
        },
        loading: null
      }
    },
    created() {
      //增加时间选框默认选中功能
      var timeTamp = new Date().getTime() - 24 * 60 * 60 * 1000
      var lastTime = new Date(timeTamp)
      this.loading = true
      this.value1 = lastTime.getFullYear() + '-' + (lastTime.getMonth() + 1) + '-' + lastTime.getDate()
      this.$http.get("keyWord/entry").then((response) => {
        this.objToArr(response.body.data)
      })
    },
    methods: {
      numchange(value) {
        this.Table.overflow = false;
        if (value > 20) {
          this.Table.overflow = true
        }
        this.$data.value6 = value
        this.inputchange()
      },
      inputchange() {
        var data1 = {
          "data_time": this.value1,
          "data_items": this.$data.value2,
          "data_choice": this.$data.value3,
          "time_length": this.$data.value5,
          "data_head": this.$data.value6
        }
        var data = JSON.stringify(data1) //格式化数据
        this.loading = true
        this.$http.post("keyWord/entry", {
          data
        }, {
          emulateJSON: true
        }).then((response) => {
          this.objToArr(response.body.data)
        })
      },
      objToArr(obj) {
        var middle_Table_body = [];
        var middle_Table_title = [];
        if (obj) {
          for (let j in obj) {
            for (let i in obj[j]) {
              middle_Table_title.push(i)
            }
            break;
          }
          for (var i in obj) {
            for (let j in obj[i]) {
              if (obj[i][j] == null) {
                obj[i][j] = ''
              } else if (j.slice(0, 2) == "日期") {
                if (this.value1[1] == "支付转化率" || this.value1[1] == "点击率") {
                  obj[i][j] = parseFloat(obj[i][j] * 100).toFixed(2) + '%'
                } else if (this.value1[1] == "相关搜索词数" || this.value1[1] == "搜索人气" || this.value1[1] == "点击人气") {
                  obj[i][j] = obj[i][j].toString().replace(/(\d)(?=(?:\d{3})+$)/g, '$1,')
                } else if (typeof (obj[i][j]) != "string" && this.value1[1] == "直通车参考价") {
                  obj[i][j] = '￥' + parseFloat(obj[i][j]).toFixed(2)
                } else {
                  obj[i][j] = obj[i][j]
                }
              } else {
                if (j == '相关搜索词数' || j == '搜索人气' || j == '点击人气') {
                  obj[i][j] = obj[i][j].toString().replace(/(\d)(?=(?:\d{3})+$)/g, '$1,')
                } else if (j == '支付转化率' || j == '点击率') {
                  obj[i][j] = parseFloat(obj[i][j] * 100).toFixed(2) + '%'
                } else if (typeof (obj[i][j]) != "string" && j == '直通车参考价') {
                  obj[i][j] = '￥' + parseFloat(obj[i][j]).toFixed(2)
                } else {
                  obj[i][j] = obj[i][j]
                }
              }
            }
            middle_Table_body.push(obj[i])
          }
          this.Table.tableData_title = middle_Table_title
          this.loading = false
          this.Table.tableData = middle_Table_body
          this.Table.tableData_prepag = this.Table.tableData.slice(0, 20) //每页默认取出20条数据
        }
      },
      handleSizeChange(val) {
        // console.log(`每页 ${val} 条`);
        var start = (this.Table.PageIndex - 1) * val //数据起始位置
        var end = this.Table.PageIndex * val //数据末端位置
        this.Table.tableData_prepag = this.Table.tableData.slice(start, end) //返回数据
        this.Table.prePageCount = val
      },
      handleCurrentChange(val) {
        // console.log(`当前页: ${val}`);
        var start = this.Table.prePageCount * (val - 1) //数据起始位置
        var end = (this.Table.prePageCount) * val //数据末端位置
        this.Table.tableData_prepag = this.Table.tableData.slice(start, end) //返回数据
        this.Table.PageIndex = val
      }
    }
  }

</script>
