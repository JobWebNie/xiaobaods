<template>
  <div>
    <el-row class="title" type="flex" justify="space-between" align="middle">
      <el-col class="title-left">
        <h3>流量产品趋势分析</h3>
      </el-col>
      <el-col class="title-right">
        <p>针对特定节点和分类，对一定时间周期内排名，订单数进行追踪</p>
      </el-col>
    </el-row>
    <el-row class="navlist" type="flex" justify="space-around" align="middle">
      <el-col class="list-left">
        <el-date-picker v-model="data.date" :picker-options="pickerOption" size='small' v-on:change="inputchange"></el-date-picker>
        <el-select v-model="data.category" size='small' v-on:change="inputchange">
          <el-option v-for="item in categoryOption" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-select v-model="data.variable" size='small' v-on:change="inputchange">
          <el-option v-for="item in variableOption" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-select v-model="data.length" size='small' v-on:change="inputchange">
          <el-option v-for="item in lengthOption" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <span class="Embellish">
          <a @click="excellCsv()">下载</a>
          <a @click.prevent="loadPicture()">图片</a>
        </span>
      </el-col>
      <el-col class="list-right">
        <el-tag v-for="tag in dynamicTags" :key="tag" :closable="true" @close="handleClose(tag)">{{tag}}</el-tag>
        <!-- <el-input size='small' @keyup.enter.native="inputchange" v-model.trim="data.titler" placeholder="商品筛选"></el-input>
        <el-input size='small' @keyup.enter.native="inputchange" v-model.trim="data.storer" placeholder="店铺搜索"></el-input>
        <el-button @click="inputchange" type="primary" size='small'>筛选</el-button>
        <el-button size='small' @click="emptyFilter">清空</el-button>-->
        <el-button @click="dialogFormVisible = true" type="primary" size='small'>筛选</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <el-table class="tablelist" v-loading="loading" :data="Table.tableData_prepag" style="width:100%;position:relative;" :height="Table.height"
          @cell-click="showPicture">
          <el-table-column prop="热销排名" label="排名" width="50" header-align="center" align="center"></el-table-column>
          <el-table-column :label="Table.tableData_title[0]" header-align="center" align="center" width="80">
            <template scope="scope">
              <a target="_blank" :href="Table.bigPicture" alt="">
                <img style="height:44px;" :src="scope.row.主图缩略图" alt="店铺图片">
              </a>
            </template>
          </el-table-column>
          <el-table-column show-overflow-tooltip :label="Table.tableData_title[2]" header-align="center" align="center">
            <template scope="scope">
              <a target="_blank" :href="scope.row.宝贝链接" alt="">{{scope.row.商品信息}}</a>
            </template>
          </el-table-column>
          <el-table-column show-overflow-tooltip prop="所属店铺" :label="Table.tableData_title[3]" header-align="center" align="center"
            width="150">
            <template scope="scope">
              <a target="_blank" :href="scope.row.店铺链接">{{scope.row.所属店铺}}</a>
            </template>
          </el-table-column>
          <el-table-column :prop="Table.tableData_title[4]" :label="Table.tableData_title[4]" :formatter="contentFormatter" header-align="right"
            align="right" width="120"></el-table-column>
          <el-table-column :prop="Table.tableData_title[5]" :label="Table.tableData_title[5]" :formatter="contentFormatter" header-align="right"
            align="right" width="120"></el-table-column>
          <el-table-column :prop="Table.tableData_title[6]" :label="Table.tableData_title[6]" :formatter="contentFormatter" header-align="right"
            align="right" width="120"></el-table-column>
          <el-table-column v-for="(title,id) in Table.tableData_title" v-if="title.slice(0,2)=='日期'" :prop="title" :render-header="renderHeader"
            :formatter="contentFormatter" align="right" header-align="right" width="50"></el-table-column>
          <el-table-column header-align="center" align="center" label="操作" width="120">
            <template scope="scope">
              <a target="_blank" :href="scope.row.查看详情" value='' alt=""> 查看详情</a>
              <br>
              <a target="_blank" :href="scope.row.同款货源" alt="">同款货源</a>
            </template>
          </el-table-column>
        </el-table>
        <transition name="page">
          <div v-show='!loading' style="text-align:center;">
            <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="Table.PageIndex" :page-sizes="[20, 50, 100]"
              :page-size="Table.prePageCount" layout="total, sizes, prev, pager, next, jumper" :total="Table.total"></el-pagination>
          </div>
        </transition>
      </el-col>
    </el-row>
    <el-dialog size="mini" title="商品筛选" :visible.sync="dialogFormVisible">
      <el-form :model="ruleForm" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="商品信息" prop="titler" :rules=" [{message: '请输入活动名称',trigger: 'blur'}]">
          <el-input v-model="ruleForm.titler" placeholder="请输入商品筛选词"></el-input>
        </el-form-item>
        <el-form-item label="所属店铺" prop="storer" :rules="[{message: '请选择活动区域',trigger: 'change'}]">
          <el-input v-model="ruleForm.storer" placeholder="请输入店铺名称"></el-input>
        </el-form-item>
        <el-form-item label="支付订单数">
          <el-col :span="4">
            <el-form-item prop="v1m" :rules="[{type: 'number',message: '订单数必须为数字值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v1m" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="2" style="text-align:center">—</el-col>
          <el-col :span="4">
            <el-form-item prop="v1l" :rules="[{ type: 'number',message: '订单数必须为数字值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v1l" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item label="交易增长幅度">
          <el-col :span="4">
            <el-form-item prop="v2m" :rules="[{type: 'number',message: '交易增长必须为数字值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v2m" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="2" style="text-align:center">%—</el-col>
          <el-col :span="4">
            <el-form-item prop="v2l" :rules="[{ type: 'number',message: '交易增长必须为数字值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v2l" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>%
        </el-form-item>
        <el-form-item label="转化率指数">
          <el-col :span="4">
            <el-form-item prop="v3m" :rules="[{type: 'number',message: '转化率指数必须为数字值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v3m" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="2" style="text-align:center">—</el-col>
          <el-col :span="4">
            <el-form-item prop="v3l" :rules="[{ type: 'number',message: '转化率指数必须为数字值',trigger: 'change'}]">
              <el-input v-model.number="ruleForm.v3l" auto-complete="off"></el-input>
            </el-form-item>
          </el-col>
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
  import {
    mapActions
  } from 'vuex'
  import {
    download
  } from '../../assets/js/download'
  export default {
    data() {
      return {
        dynamicTags: [],
        dialogFormVisible: false,
        ruleForm: {
          titler: '',
          storer: '',
          v1l: 0,
          v1m: 0,
          v2m: 0,
          v2l: 0,
          v3m: 0,
          v3l: 0
        },
        // Tvalue: Date.now()- 8.64e7,
        pickerOption: {
          disabledDate(time) {
            var min = Date.parse('2016-11-24')
            var max = Date.now() - 8.64e7;
            if (time.getTime() > max || time.getTime() < min) {
              return true;
            } else {
              return false;
            }
          }
        },
        categoryOption: [{
          label: '类目：牛仔裤',
          value: '牛仔裤'
        }, {
          label: '类目：休闲裤',
          value: '休闲裤'
        }, {
          label: '类目：打底裤',
          value: '打底裤'
        }],
        variableOption: [{
          value: '热销排名',
          label: '趋势：热销排名'
        }, {
          value: '流量指数',
          label: '趋势：流量指数'
        }, {
          value: '搜索人气',
          label: '趋势：搜索人气'
        }, {
          value: '支付子订单数',
          label: '趋势：支付子订单数'
        }],
        lengthOption: [{
          value: 7,
          label: '天数：近7天'
        }, {
          value: 14,
          label: '天数：近14天'
        }],
        Table: {
          tableData_title: [],
          tableData_prepag: [],
          prePageCount: 20,
          PageIndex: 1,
          height: 820,
          bigPicture: null,
          total: null
        },
        data: {
          fun: 'a',
          date: Date.now() - 8.64e7,
          length: 7,
          category: '牛仔裤',
          variable: '热销排名',
          line_f: 0,
          line_b: 20,
          table: 'bc_attribute_granularity_visitor'
        },
        loading: true,
        fullpath: ''
      }
    },
    mounted() {
      // 显示遮罩层加载功能
      this.$http.get("prod/search").then((response) => {
        this.fullpath = response.body.fullpath
        this.objToArr(response.body.data)
        this.loading = false
      })
    },
    methods: {
      ...mapActions(['PICTURE_INSERT']),
      excellCsv() {
        download(this.fullpath)
      },
      renderHeader(h, {
        column,
        $index
      }) { //在不改变json数据的情况下改变header
        var th = column.property.slice(-4, -2) + '-' + column.property.slice(-2)
        return column.label = th;
      },
      contentFormatter(row, column, cellValue) {
        let reg = String(cellValue).replace(/(\d)(?=(?:\d{3})+$)/g, '$1,')
        let percent = Math.round(cellValue * 100) + '%'
        if (column.property.slice(0, 2) == "日期") {
          if (cellValue == null) {
            return ''
          } else {
            const fm = this.data.variable
            switch (fm) {
              case '支付子订单数':
                return cellValue = reg;
                break;
              case '搜索人气':
                return cellValue = reg;
                break;
              case '流量指数':
                return cellValue = reg;
                break;
              default:
                return cellValue = cellValue;
                break;
            }
          }
        } else {
          switch (column.property) {
            case '支付子订单数':
              return cellValue = reg;
              break;
            case '搜索人气':
              return cellValue = reg;
              break;
            case '流量指数':
              return cellValue = reg;
              break;
            default:
              return cellValue = cellValue;
              break;
          }
        }
      },
      inputchange() {
        this.loading = true
        var compile = Object.assign({}, this.data, this.ruleForm)
        compile.titler = compile.titler.replace(/\s+/g, '|') //实现空格匹配多个
        compile.storer = compile.storer.replace(/\s+/g, '|')
        compile.v2l = compile.v2l / 100
        compile.v2m = compile.v2m / 100
        var data = JSON.stringify(compile)
        this.$http.post("prod/search", {
          data
        }, {
          emulateJSON: true
        }).then((response) => {
          this.loading = false
          if (response.body.code == 200) {
            this.fullpath = response.body.fullpath
            this.objToArr(response.body.data)
          } else {

            this.$message({
              message: response.body.msg,
              type: 'warning'
            });
          }
        })
      },
      objToArr(obj) {
        var middle_Table_body = [];
        var middle_Table_title = [];
        if (obj) {
          for (let j in obj) {
            for (let k in obj[j]) {
              if (k == 'total') {
                this.Table.total = obj[j][k]
              } else {
                middle_Table_title.push(k)
              }
            }
            break;
          }
          for (let i in obj) {
            middle_Table_body.push(obj[i])
          }
          this.Table.tableData_title = middle_Table_title
          this.Table.tableData_prepag = middle_Table_body

        }
      },
      handleSizeChange(val) {
        // console.log(`每页 ${val} 条`);
        this.Table.prePageCount = val
        this.data.line_b = (this.Table.PageIndex - 1) * val
        this.data.line_f = this.Table.PageIndex * val
        this.inputchange()
      },
      handleCurrentChange(val) {
        // console.log(`当前页: ${val}`);
        this.Table.PageIndex = val
        this.data.line_b = this.Table.prePageCount * (val - 1)
        this.data.line_f = this.Table.prePageCount * val
        this.inputchange()

      },
      showPicture(row, cell) {
        if (cell.label == "主图缩略图") {
          this.Table.bigPicture = row.主图缩略图.slice(0, -10)
        }
      },
      // emptyFilter() {
      //   this.data.storer =''
      //   this.data.titler = ''
      //   this.inputchange()
      // },
      loadPicture() {
        this.PICTURE_INSERT(this.Table.tableData_prepag) //数据存入store,详情请见
        window.router.push({
          path: '/picture/download/'
        })
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
        this.dynamicTags = []
        this.inputchange()
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          this.dynamicTags = []
          if (valid) {
            for (var ite in this.ruleForm) {
              var _this = this
              var idhas = this.dynamicTags.some(function (item) {
                if (item.split('：')[1] == _this.ruleForm[ite]) {
                  return true
                }
              })
              if (!idhas && this.ruleForm[ite] != '' && this.ruleForm[ite] != null) {
                if (ite == 'titler') {
                  this.dynamicTags.push('商品信息：' + this.ruleForm[ite])
                } else if (ite == 'storer') {
                  this.dynamicTags.push('所属店铺：' + this.ruleForm[ite])
                } else if (ite == 'v1m') {
                  this.dynamicTags.push('订单多于：' + this.ruleForm[ite])
                } else if (ite == 'v1l') {
                  this.dynamicTags.push('订单少于：' + this.ruleForm[ite])
                } else if (ite == 'v2m') {
                  this.dynamicTags.push('增长率高于：' + this.ruleForm[ite])
                } else if (ite == 'v2l') {
                  this.dynamicTags.push('增长率低于：' + this.ruleForm[ite])
                } else if (ite == 'v3m') {
                  this.dynamicTags.push('转化高于：' + this.ruleForm[ite])
                } else {
                  this.dynamicTags.push('转化低于：' + this.ruleForm[ite])
                }
              }
            }
            this.inputchange()
            this.dialogFormVisible = false
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      handleClose(tag) {

        this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
      }
    }
  }

</script>
