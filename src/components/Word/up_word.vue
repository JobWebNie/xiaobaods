<template>
  <div>
    <el-row class="title" type="flex" justify="space-between" align="middle">
      <el-col class="title-left">
        <h3>飙升词分析</h3>
      </el-col>
      <el-col class="title-right">
        <p>针对特定飙升词，对一定周期内飙升词，飙升词进行排名</p>
      </el-col>
    </el-row>
    <el-row class="navlist" type="flex" justify="space-around" align="middle">
      <el-col class="list-left">
        <el-date-picker v-model="data.date" :picker-options="pickerOption" size='small' v-on:change="inputchange"></el-date-picker>
        <el-select v-model="data.category" size='small' v-on:change="inputchange">
          <el-option v-for="item in options0" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-cascader v-model="data.data_reorder" :options="options1" size='small' v-on:change="inputchange"></el-cascader>
        <el-select v-model="data.length" size='small' v-on:change="inputchange">
          <el-option v-for="item in options4" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <span class="Embellish">
          <a :href='fullpath'>下载</a>
        </span>
      </el-col>
      <el-col class="list-right">
        <el-tag v-for="tag in dynamicTags" :key="tag" :closable="true" @close="handleClose(tag)">{{tag}}</el-tag>
        <el-button @click="dialogFormVisible = true" type="primary" size='small'>筛选</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <el-table class="tablelist" v-loading="loading" :data="Table.tableData_prepag" :height="this.Table.height">
          <el-table-column v-for="title in Table.tableData_title" v-if="title.name!=='total'" :prop="title.name" :render-header="renderHeader"
            :formatter="contentFormatter" align="center" header-align="center" :min-width="title.width"></el-table-column>
        </el-table>
        <div style="position:relative; text-align:center;">
          <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="Table.PageIndex" :page-sizes="[15, 20, 50, 100]"
            :page-size="Table.prePageCount" layout="total, sizes, prev, pager, next, jumper" :total="Table.total">
          </el-pagination>
        </div>
      </el-col>
    </el-row>
    <el-dialog size="mini" title="飙升核心词" :visible.sync="dialogFormVisible">
      <el-form :model="ruleForm" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="搜索词" prop="titler" :rules=" [{message: '请输入搜索词',trigger: 'blur'}]">
          <el-input v-model="ruleForm.titler" placeholder="请输入搜索词"></el-input>
        </el-form-item>
        <el-form-item label="相关搜索词数">
          <el-col :span="4">
            <el-form-item prop="v1m" :rules="[{type: 'number',message: '搜索词数为数值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v1m" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="2" style="text-align:center">—</el-col>
          <el-col :span="4">
            <el-form-item prop="v1l" :rules="[{ type: 'number',message: '搜索词数为数值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v1l" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item label="搜索人气">
          <el-col :span="4">
            <el-form-item prop="v2m" :rules="[{type: 'number',message: '搜索人气填写数字值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v2m" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="2" style="text-align:center">—</el-col>
          <el-col :span="4">
            <el-form-item prop="v2l" :rules="[{ type: 'number',message: '搜索人气填写数字值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v2l" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item label="词搜索增幅">
          <el-col :span="4">
            <el-form-item prop="v3m" :rules="[{type: 'number',message: '词搜索增幅填写数字值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v3m" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="2" style="text-align:center">%—</el-col>
          <el-col :span="4">
            <el-form-item prop="v3l" :rules="[{ type: 'number',message: '词搜索增幅填写数字值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v3l" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>%
        </el-form-item>

        <el-form-item label="点击人气">
          <el-col :span="4">
            <el-form-item prop="v4m" :rules="[{type: 'number',message: '点击人气填写数字值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v4m" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="2" style="text-align:center">—</el-col>
          <el-col :span="4">
            <el-form-item prop="v4l" :rules="[{ type: 'number',message: '点击人气填写数字值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v4l" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item label="支付转化率">
          <el-col :span="4">
            <el-form-item prop="v5m" :rules="[{type: 'number',message: '转化率指数必须为数字值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v5m" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="2" style="text-align:center">%—</el-col>
          <el-col :span="4">
            <el-form-item prop="v5l" :rules="[{ type: 'number',message: '转化率指数必须为数字值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v5l" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>%
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button @click="resetForm('ruleForm')">重置</el-button>
        <el-button type="primary" @click="submitForm('ruleForm')"> 筛选商品</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        dynamicTags: [],
        dialogFormVisible: false,
        ruleForm: {
          titler: '',
          v1l: 0,
          v1m: 0,
          v2m: 0,
          v2l: 0,
          v3m: 0,
          v3l: 0,
          v4m: 0,
          v4l: 0,
          v5m: 0,
          v5l: 0
        },
        pickerOption: {
          disabledDate(time) {
            var min = Date.parse('2016-12-11')
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
          value: '飙升核心词',
          label: '飙升核心词',
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
            value: '词均搜索增长幅度',
            label: '词均搜索增长幅度'
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
          value: '飙升修饰词',
          label: '飙升修饰词',
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
            value: '词均搜索增长幅度',
            label: '词均搜索增长幅度'
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
          value: '飙升品牌词',
          label: '飙升品牌词',
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
            value: '词均搜索增长幅度',
            label: '词均搜索增长幅度'
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
          value: '飙升搜索词',
          label: '飙升搜索词',
          children: [{
            value: '排名',
            label: '排名'
          }, {
            value: '搜索人气',
            label: '搜索人气',
          }, {
            value: '搜索增长幅度',
            label: '搜索增长幅度'
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
          value: '飙升长尾词',
          label: '飙升长尾词',
          children: [{
            value: '排名',
            label: '排名'
          }, {
            value: '搜索人气',
            label: '搜索人气',
          }, {
            value: '搜索增长幅度',
            label: '搜索增长幅度'
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
        data: {
          fun: 'w',
          line_f: 0,
          line_b: 20,
          date: Date.now() - 8.64e7,
          category: '牛仔裤',
          data_reorder: ["飙升核心词", "排名"],
          length: 7
        },
        Table: {
          total: null,
          tableData_title: [],
          tableData_prepag: [],
          prePageCount: 20,
          PageIndex: 1,
          height: 840
        },
        fullpath: '',
        loading: false
      }
    },
    created() {
      //增加时间选框默认选中功能
      this.loading = true
      this.$http.get("keyWord/up").then((response) => {
        this.fullpath = response.body.fullpath
        this.objToArr(response.body.data)
        this.loading = false
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
        let percent = Math.round(cellValue * 100) + '%'
        if (column.property.slice(0, 2) == "日期") {
          const fm = this.data.data_reorder[1]
          switch (fm) {
            case '支付转化率':
              return cellValue = percent;
              break;
            case '点击率':
              return cellValue = percent;
              break;
            case '词均搜索增长幅度':
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
            case '词均搜索增长幅度':
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
        var compile = Object.assign({}, this.data, this.ruleForm)
        compile.choice = compile.data_reorder[0]
        compile.variable = compile.data_reorder[1]
        compile.v3m = compile.v3m / 100
        compile.v3l = compile.v3l / 100
        compile.v5m = compile.v5m / 100
        compile.v5l = compile.v5l / 100
        delete compile.data_reorder
        var data = JSON.stringify(compile) //格式化数据
        this.loading = true
        this.$http.post("keyWord/up", {
          data
        }, {
          emulateJSON: true
        }).then((response) => {
          this.loading = false
          this.fullpath = response.body.fullpath
          this.objToArr(response.body.data)
        })
      },
      objToArr(obj) {
        var middle_Table_body = [];
        var middle_Table_title = [];
        if (obj) {
            for (let i in obj) {
            for (let j in obj[i]) {
              if (j == 'total') {
                this.Table.total = obj[i][j]
              } else {
                switch (j) {
                  case '相关搜索词数':
                    middle_Table_title.push({
                      name: j,
                      width: '80'
                    });
                    break;
                  case '词均搜索增长幅度':
                    middle_Table_title.push({
                      name: j,
                      width: '80'
                    });
                    break;
                  case '直通车参考价':
                    middle_Table_title.push({
                      name: j,
                      width: '80'
                    });
                    break;
                  default:
                    middle_Table_title.push({
                      name: j,
                      width: '50'
                    });
                    break;
                }
              }
            }
            break;
          }
          for (var i in obj) {
            middle_Table_body.push(obj[i])
          }
          
        }
        this.loading = false
        this.Table.tableData_title = middle_Table_title
        this.Table.tableData_prepag = middle_Table_body
      },
      handleSizeChange(val) {
        this.Table.prePageCount = val
        this.data.line_b = (this.Table.PageIndex - 1) * val
        this.data.line_f = this.Table.PageIndex * val
        this.inputchange()
      },
      handleCurrentChange(val) {
        this.Table.PageIndex = val
        this.data.line_b = this.Table.prePageCount * (val - 1)
        this.data.line_f = this.Table.prePageCount * val
        this.inputchange()
      }
    }
  }

</script>
<style scoped>
  .el-table__body,
  .el-table__header {
    table-layout: unset;
  }

</style>
