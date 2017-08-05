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
        <el-date-picker v-model="value3" :picker-options="pickerOption"  v-on:change="inputchange" size='small'></el-date-picker>
        <el-cascader v-model="value0" :options="options0" size='small'  v-on:change="inputchange"></el-cascader>
          <el-select v-model="value1" size='small'  v-on:change="inputchange">
          <el-option v-for="item in options1" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-select v-model="value2" size='small'  v-on:change="inputchange">
          <el-option v-for="item in options2" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-col>
      <el-col class="list-right">
        <el-input size='small' @keyup.enter.native="inputchange" v-model.trim="value5" placeholder="商品筛选"></el-input>
        <el-autocomplete size='small' v-model.trim="value4" :fetch-suggestions="querySearchAsync" @keyup.enter.native="inputchange"
          placeholder="店铺筛选"></el-autocomplete>
        <el-button @click="inputchange" type="primary" size='small'>筛选</el-button>
        <el-button size='small' @click="emptyFilter">清空</el-button>
      </el-col>
    </el-row>

    <el-row>
      <el-col>
        <el-table v-loading="loading" :data="Table.tableData_prepag" style="width: 100%" :height="this.Table.height" @cell-click="showPicture">
          <el-table-column prop="热销排名" label="排名" width="50" header-align="center" align="center"></el-table-column>
          <el-table-column :label="Table.tableData_title[0]" header-align="center" align="center">
            <template scope="scope">
              <a target="_blank" :href="Table.bigPicture" alt=""><img style="height:44px;" :src="scope.row.主图缩略图" alt="">
            </a></template>
          </el-table-column>
          <el-table-column show-overflow-tooltip :label="Table.tableData_title[2]" header-align="center" align="center">
            <template scope="scope"><a target="_blank" :href="scope.row.宝贝链接" alt="">{{scope.row.商品信息}}</a></template>
          </el-table-column>
          <el-table-column show-overflow-tooltip prop="所属店铺" :label="Table.tableData_title[3]" header-align="center" align="center">
            <template scope="scope"><a target="_blank" :href="scope.row.店铺链接">{{scope.row.所属店铺}}</a></template>
          </el-table-column>
          <el-table-column :prop="Table.tableData_title[4]" :label="Table.tableData_title[4]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[5]" :label="Table.tableData_title[5]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[6]" :label="Table.tableData_title[6]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[10]" :label="Table.tableData_title[10]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[11]" :label="Table.tableData_title[11]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[12]" :label="Table.tableData_title[12]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[13]" :label="Table.tableData_title[13]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[14]" :label="Table.tableData_title[14]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[15]" :label="Table.tableData_title[15]" header-align="right" align="right"></el-table-column>
          <el-table-column :prop="Table.tableData_title[16]" :label="Table.tableData_title[16]" header-align="right" align="right"></el-table-column>
          <el-table-column v-if="Table.tableData_title[17]" :prop="Table.tableData_title[17]" :label="Table.tableData_title[17]" header-align="right"
            align="right"></el-table-column>
          <el-table-column v-if="Table.tableData_title[18]" :prop="Table.tableData_title[18]" :label="Table.tableData_title[18]" header-align="right"
            align="right"></el-table-column>
          <el-table-column v-if="Table.tableData_title[19]" :prop="Table.tableData_title[19]" :label="Table.tableData_title[19]" header-align="right"
            align="right"></el-table-column>
          <el-table-column v-if="Table.tableData_title[20]" :prop="Table.tableData_title[20]" :label="Table.tableData_title[20]" header-align="right"
            align="right"> </el-table-column>
          <el-table-column v-if="Table.tableData_title[21]" :prop="Table.tableData_title[21]" :label="Table.tableData_title[21]" header-align="right"
            align="right"></el-table-column>
          <el-table-column v-if="Table.tableData_title[22]" :prop="Table.tableData_title[22]" :label="Table.tableData_title[22]" header-align="right"
            align="right"></el-table-column>
          <el-table-column v-if="Table.tableData_title[23]" :prop="Table.tableData_title[23]" :label="Table.tableData_title[23]" header-align="right"
            align="right"></el-table-column>
          <el-table-column v-if="Table.tableData_title[24]" :prop="Table.tableData_title[24]" :label="Table.tableData_title[24]" header-align="right"
            align="right"> </el-table-column>
          <el-table-column header-align="center" align="center" label="操作">
            <template scope="scope">
              <a target="_blank" :href="scope.row.查看详情" value='' alt=""> 查看详情</a><br></template>
          </el-table-column>
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
        value3: '',
        pickerOption: {
          disabledDate(time) {
            var min =Date.parse('2016-11-24')
            var max = Date.now() - 8.64e7;
            if (time.getTime() > max || time.getTime() < min) {
              return true;
            } else {
              return false;
            }
          }
        },
        value0: ['牛仔裤', '款式', '铅笔裤'],
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
        value1: "热销排名",
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
        value2: 7,
        options2: [{
          value: 7,
          label: '显示周期：近7天'
        }, {
          value: 14,
          label: '显示周期：近14天'
        }],
        Table: {
          tableData: [],
          tableData_title: [],
          tableData_prepag: [],
          prePageCount: 15,
          bigPicture: null,
          PageIndex: 1,
          height: 823
        },
        loading: false,
        restaurants: [],
        value4: '',
        value5: ''
      }
    },
    created() {
      //增加时间选框默认选中功能
      var timeTamp = new Date().getTime() - 24 * 60 * 60 * 1000
      var lastTime = new Date(timeTamp)
      this.value3 = lastTime.getFullYear() + '-' + (lastTime.getMonth() + 1) + '-' + lastTime.getDate()
      //显示遮罩层加载功能
      this.loading = true
      this.$http.get("market/prop").then((response) => {
        this.objToArr(response.body.data)
      })
      this.$http.get("shop/search").then((response) => {
        for (var i = 0; i < response.body.data.length; i++) {
          this.restaurants.push(new Object({
            value: response.body.data[i]
          }))
        }
      })
    },
    methods: {
      inputchange() {
        this.loading = true
        var data1 = {
          "data_time": this.value3,
          "data_items": this.$data.value0,
          "data_reorder": this.$data.value1,
          "choice": this.$data.value4,
          "titlechoice": this.$data.value5,
          "data_time_length": this.$data.value2
        }
        var data = JSON.stringify(data1) //格式化数据
        this.$http.post("market/prop", {
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
          for (let j in obj[0]) {
            middle_Table_title.push(j)
          }
          for (let i in obj) {
            middle_Table_body.push(obj[i])
          }
          this.loading = false
          this.Table.tableData_title = middle_Table_title
          this.Table.tableData = middle_Table_body
          this.Table.tableData_prepag = this.Table.tableData.slice(0, 15)
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
      },
      showPicture(row) {
        this.Table.bigPicture = row.主图缩略图.slice(0, -10)
      },
      querySearchAsync(queryString, cb) {
        var restaurants = this.restaurants
        var results = queryString ? restaurants.filter(this.createStateFilter(queryString)) : restaurants;
        clearTimeout(this.timeout);
        this.timeout = setTimeout(() => {
          cb(results);
        });
      },
      emptyFilter() {
        this.value4 = ''
        this.value5 = ''
        this.inputchange()
      },
    }
  }

</script>
