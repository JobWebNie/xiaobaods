<template>
  <div>
    <el-row class="title" type="flex" justify="space-between" align="middle">
      <el-col class="title-left">
        <h3>属性详情</h3>
      </el-col>
      <el-col class="title-right">
        <p>详情页数据一览表</p>
      </el-col>
    </el-row>
    <el-row class="navlist" type="flex" justify="space-around" align="middle">
      <el-col class="list-left">
        <el-date-picker v-model=" data.date" :picker-options="pickerOption" v-on:change="inputchange" size='small'></el-date-picker>
        <el-cascader v-model=" data.category" :options="options0" size='small' v-on:change="inputchange"></el-cascader>
        <el-select v-model=" data.variable" size='small' v-on:change="inputchange">
          <el-option v-for="item in options1" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-select v-model=" data.length" size='small' v-on:change="inputchange">
          <el-option v-for="item in options2" :label="item.label" :value="item.value"></el-option>
        </el-select>
         <span class="Embellish"><a @click="excellCsv()">下载</a></span>
          <span class="Embellish"><a @click.prevent="loadPicture(Table.tableData)">图片</a></span>
      </el-col>
      <el-col class="list-right" style="width:40%;text-align:right;">
      <el-tag v-for="tag in dynamicTags" :key="tag" :closable="true" @close="handleClose(tag)">{{tag}}</el-tag>
     <!-- <span v-if="false">
        <el-input size='small' @keyup.enter.native="inputchange" v-model.trim="data.titlechoice" placeholder="商品筛选"></el-input>
        <el-input size='small' @keyup.enter.native="inputchange" v-model.trim="data.storechoice" placeholder="店铺搜索"></el-input>
        <el-autocomplete size='small' v-model="data.storegroupchoice" :fetch-suggestions="querySearchAsync" @keyup.enter.native="inputchange" placeholder="热门店铺分类"></el-autocomplete>
        <el-button @click="inputchange" type="primary" size='small'>筛选</el-button>
        <el-button size='small' @click="emptyFilter">清空</el-button>
      </span>-->
      <el-button @click="dialogFormVisible = true" type="primary" size='small'>筛选</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <el-table v-loading="loading" :data="Table.tableData_prepag" style="width: 100%" :height="this.Table.height" @cell-click="showPicture">
          <el-table-column prop="热销排名" label="排名" width="50" header-align="center" align="center"></el-table-column>
          <el-table-column :label="Table.tableData_title[0]" header-align="center" align="center" width="80">
            <template scope="scope"><a target="_blank" :href="Table.bigPicture" alt=""><img style="height:44px;" :src="scope.row.主图缩略图" alt=""></a></template>
          </el-table-column>
          <el-table-column show-overflow-tooltip :label="Table.tableData_title[2]" header-align="center" align="center">
            <template scope="scope"><a target="_blank" :href="scope.row.宝贝链接" alt="">{{scope.row.商品信息}}</a></template>
          </el-table-column>
          <el-table-column show-overflow-tooltip prop="所属店铺" :label="Table.tableData_title[3]" header-align="center" align="center"
            width="150">
            <template scope="scope"><a target="_blank" :href="scope.row.店铺链接">{{scope.row.所属店铺}}</a></template>
          </el-table-column>
          <el-table-column :prop="Table.tableData_title[4]" :label="Table.tableData_title[4]" :formatter="contentFormatter" header-align="right" align="right" width="120"></el-table-column>
          <el-table-column :prop="Table.tableData_title[5]" :label="Table.tableData_title[5]" :formatter="contentFormatter" header-align="right" align="right" width="120"></el-table-column>
          <el-table-column :prop="Table.tableData_title[6]" :label="Table.tableData_title[6]" :formatter="contentFormatter" header-align="right" align="right" width="120"></el-table-column>
          <el-table-column v-for="title in Table.tableData_title" v-if="title.slice(0,2)=='日期'" :prop="title" :render-header="renderHeader"  :formatter="contentFormatter"
            width="50" header-align="right" align="right"></el-table-column>
          <el-table-column header-align="center" align="center" label="操作" width="120">
            <template scope="scope"><a target="_blank" :href="scope.row.查看详情" value='' alt=""> 查看详情</a><br></template>
          </el-table-column>
        </el-table>
        <div style="position:relative; text-align:center;">
          <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="Table.PageIndex" :page-sizes="[20, 50, 100]"
            :page-size="Table.prePageCount" layout="total, sizes, prev, pager, next, jumper" :total="Table.total">
          </el-pagination>
        </div>
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
    PICTURE_INSERT
  } from '../../store/picture'
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
        options0: [{
          label: '牛仔裤',
          value: '牛仔裤',
          children: [{
              value: '款式',
              label: '款式',
              children: [{
                  value: '铅笔裤',
                  label: '铅笔裤'
                }, {
                  value: '哈伦裤',
                  label: '哈伦裤'
                }, {
                  value: '阔脚裤',
                  label: '阔脚裤'
                },
                {
                  value: '连衣裤',
                  label: '连衣裤'
                }, {
                  value: '背带裤',
                  label: '背带裤'
                }, {
                  value: '直筒',
                  label: '直筒'
                }, {
                  value: '灯笼裤',
                  label: '灯笼裤',
                },
                {
                  value: '微喇裤',
                  label: '微喇裤'
                }, {
                  value: '工装裤',
                  label: '工装裤'
                }, {
                  value: '垮裤',
                  label: '垮裤'
                }
              ]
            },
            {
              value: '厚薄',
              label: '厚薄',
              children: [{
                value: '超薄',
                label: '超薄'
              }, {
                value: '薄款',
                label: '薄款'
              }, {
                value: '常规',
                label: '常规'
              }, {
                value: '加厚',
                label: '加厚'
              }]
            },
            {
              value: '裤长',
              label: '裤长',
              children: [{
                  value: '长裤',
                  label: '长裤'
                }, {
                  value: '短裤',
                  label: '短裤'
                }, {
                  value: '超短裤',
                  label: '超短裤'
                },
                {
                  value: '五分裤',
                  label: '五分裤'
                }, {
                  value: '九分裤',
                  label: '九分裤'
                }, {
                  value: '七分裤',
                  label: '七分裤'
                }
              ]
            },
            {
              value: '腰型',
              label: '腰型',
              children: [{
                value: '高腰',
                label: '高腰'
              }, {
                value: '低腰',
                label: '低腰'
              }, {
                value: '中腰',
                label: '中腰'
              }]
            }
          ]
        }, {
          label: '打底裤',
          value: '打底裤',
          children: [{
              value: '厚薄',
              label: '厚薄',
              children: [{
                value: '薄款',
                label: '薄款'
              }, {
                value: '常规',
                label: '常规'
              }, {
                value: '加绒',
                label: '加绒',
              }, {
                value: '加厚',
                label: '加厚'
              }]
            },
            {
              value: '裤长',
              label: '裤长',
              children: [{
                value: '长裤',
                label: '长裤'
              }, {
                value: '短裤',
                label: '短裤'
              }, {
                value: '七分裤/九分裤',
                label: '七分裤/九分裤'
              }]
            }
          ]
        }],
        options1: [{
          value: '热销排名',
          label: '热销排名'
        }, {
          value: '支付子订单数',
          label: '支付子订单数'
        }, {
          value: '支付件数',
          label: '支付件数'

        }, {
          value: '支付转化率指数',
          label: '支付转化率指数'
        }],
        options2: [{
          value: 7,
          label: '显示周期：近7天'
        }, {
          value: 14,
          label: '显示周期：近14天'
        }],
        Table: {
          tableData_title: [],
          tableData_prepag: [],
          prePageCount: 20,
          bigPicture: null,
          PageIndex: 1,
          height: 835
        },
        data:{
           fun: 'c',
            date:Date.now()- 8.64e7,
            length:  7,
            category: ['牛仔裤', '款式', '铅笔裤'],
            variable: '热销排名',
            storegroupchoice: '',
            line_f: 0,
            line_b: 20,
            table: 'bc_attribute_granularity_sales'
        },
        loading: true,
        // restaurants: [],
        timeout: null,
        fullpath: ''
      }
    },
    created() {
      //显示遮罩层加载功能
        this.$http.get("market/prop").then((response) => {
          this.fullpath = response.body.fullpath
          this.objToArr(response.body.data)
          this.loading = false
        })
    },
    methods: {
      ...mapActions([PICTURE_INSERT]),
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
         if(cellValue){
            return String(cellValue).replace(/(\d)(?=(?:\d{3})+$)/g, '$1,')
              
         }
      },
      inputchange() {
         this.loading = true
            var data1 = {
          date:this.data.date,
          length:this.data.length,
          variable:this.data.variable,
          category:this.data.category[0],
          classfication:this.data.category[1],
          attributes:this.data.category[2],
          table:this.data.table
        }
        var compile = Object.assign({}, data1, this.ruleForm)
        compile.titler = compile.titler.replace(/\s+/g, '|') //实现空格匹配多个
        compile.storer = compile.storer.replace(/\s+/g, '|')
        compile.v2l = compile.v2l / 100
        compile.v2m = compile.v2m / 100
        var data = JSON.stringify(compile)
        this.$http.post("market/prop",{data},{emulateJSON:true}).then((response) => {
          this.fullpath = response.body.fullpath
          this.objToArr(response.body.data)
          this.loading = false
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
      showPicture(row) {
        if (cell.label == "主图缩略图") {
          this.Table.bigPicture = row.主图缩略图.slice(0, -10)
        }
      },
      loadPicture(data) {
        this.PICTURE_INSERT(data) //数据存入store,详情请见
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
