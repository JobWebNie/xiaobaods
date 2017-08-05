<template>
  <div>
    <el-row class="title" type="flex" justify="space-between" align="middle">
      <el-col class="title-left">
        <h3>热搜词分析</h3>
      </el-col>
      <el-col class="title-right">
        <p>针对特定热搜词，对一定周期内热搜关键词进行排名</p>
      </el-col>
    </el-row>
    <el-row class="navlist" type="flex" justify="space-around" align="middle">
      <el-col class="list-left">
        <el-date-picker v-model="inputValue.data_time" :picker-options="pickerOption" size='small' v-on:change="inputchange"></el-date-picker>
        <el-select v-model="inputValue.data_items" size='small' v-on:change="inputchange">
          <el-option v-for="item in options0" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-cascader v-model="inputValue.data_reorder" :options="options1" size='small' v-on:change="inputchange"></el-cascader>
        <el-select v-model="inputValue.data_time_length" size='small' v-on:change="inputchange">
          <el-option v-for="item in options4" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <span class="Embellish"><a :href="filename">下载</a></span>
      </el-col>
      <el-col class="list-right"></el-col>
    </el-row>
    <el-row>
      <el-col>
        <el-table class="tablelist" v-loading="loading" :data="Table.tableData_prepag" style="width: 100%;position:relative;" :height="this.Table.height">
        <el-table-column v-for="title in Table.tableData_title" :prop="title.name" :render-header="renderHeader" :formatter="contentFormatter"
            :min-width="title.width" align="center" header-align="center" :resizable="false"></el-table-column>
        </el-table>
        <div style="position:relative; text-align:center;">
          <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="Table.PageIndex" :page-sizes="[15, 20, 50, 100]"
            :page-size="Table.prePageCount" layout="total, sizes, prev, pager, next, jumper" :total="Table.tableData.length">
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
        pickerOption: {
          disabledDate(time) {
            var min =  Date.parse('2016-12-11')
            var max = Date.now() - 8.64e7;
            if (time.getTime() > max || time.getTime() < min) {
              return true;
            } else {
              return false;
            }
          }
        },
        options0: [{
          label: '类目：牛仔裤',
          value: '牛仔裤'
        }, {
          label: '类目：休闲裤',
          value: '休闲裤'
        }, {
          label: '类目：打底裤',
          value: '打底裤'
        }],
        options1: [{
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
        options4: [{
          value: 7,
          label: '显示周期：近7天'
        }, {
          value: 14,
          label: '显示周期：近14天'
        }],
        inputValue:{
          data_time: '',
          data_items: '牛仔裤',
          data_reorder:  ["热搜核心词", "排名"],
          data_time_length: 7
        },
        Table: {
          tableData: [],
          tableData_title: [],
          tableData_prepag: [],
          prePageCount: 20,
          PageIndex: 1,
          height: 840
        },
        loading: false,
        filename: ''
      }
    },
    created() {
      //增加时间选框默认选中功能
      this.inputValue.data_time= Date.now() -8.64e7
      this.loading = true
      this.$http.get("keyWord/hot").then((response) => {
      this.filename = './static/public/' + response.body.filename + '.csv'
      this.objToArr(response.body.data)
      })
    },
    methods: {
      renderHeader(h, t) { //在不改变json数据的情况下改变header
        var tf = t.$index < 8
        var th = t.column.property.slice(-4, -2) + '-' + t.column.property.slice(-2)
        switch (tf) {
          case true:
            return t.column.label = t.column.property;
            break;
          case false:
            return t.column.label = th;
            break;
        }
      },
      contentFormatter(row, column, cellValue) {
        let reg = String(cellValue).replace(/(\d)(?=(?:\d{3})+$)/g, '$1,')
        let percent= Math.round(cellValue * 100) + '%'
        if (column.property.slice(0, 2) == "日期") {
          const fm = this.inputValue.data_reorder[1]
          switch (fm) {
            case '支付转化率':
              return cellValue = percent;
              break;
            case '点击率':
              return cellValue = percent;
              break;
            case '相关搜索词数':
              return cellValue = reg;
              break;
            case '搜索人气':
              return cellValue = reg;
              break;
            case '点击人气':
              return cellValue = reg;
              break;
            case '直通车参考价':
              return cellValue = '￥' + parseFloat(cellValue).toFixed(2);
              break;
            default:
              return cellValue = cellValue;
              break;
          }
        } else {
          switch (column.property) {
            case '支付转化率':
              return cellValue = percent;
              break;
            case '点击率':
              return cellValue = percent;
              break;
            case '相关搜索词数':
              return cellValue = reg;
              break;
            case '搜索人气':
              return cellValue = reg;
              break;
            case '点击人气':
              return cellValue = reg;
              break;
            case '直通车参考价':
              return cellValue = '￥' + parseFloat(cellValue).toFixed(2);
              break;
            default:
              return cellValue = cellValue;
              break;
          }
        }
      },
    inputchange() {
        var data = JSON.stringify(this.inputValue) //格式化数据
        this.loading = true
        this.$http.post("keyWord/hot", {
          data
        }, {
          emulateJSON: true
        }).then((response) => {
          this.objToArr(response.body.data)
        })
      },
      objToArr(obj) {
         this.Table.tableData_title=[]
          this.Table.tableData=[]
        if (obj) {
          for (var i in obj) {
            this.Table.tableData.push(obj[i])
          }
          for (var j in this.Table.tableData[0]) {
            switch (j) {
              case '相关搜索词数':
                this.Table.tableData_title.push({
                  name: j,
                  width: '80'
                });
                break;
              case '直通车参考价':
                this.Table.tableData_title.push({
                  name: j,
                  width: '80'
                });
                break;
              default:
                this.Table.tableData_title.push({
                  name: j,
                  width: '50'
                });
                break;
            }
          }
          this.loading = false
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
