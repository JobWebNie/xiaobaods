<template>
  <div>
    <el-row class="title" type="flex" justify="space-between" align="middle">
      <el-col class="title-left">
        <h3>热销产品趋势分析</h3>
      </el-col>
      <el-col class="title-right">
        <p>针对特定节点和分类，对一定时间周期内排名，订单数进行追踪</p>
      </el-col>
    </el-row>
    <el-row class="navlist" type="flex" justify="space-around" align="middle">
      <el-col class="list-left">
        <el-date-picker v-model="Tvalue" :picker-options="pickerOption" size='small' v-on:change="inputchange"></el-date-picker>
        <el-select v-for="items in inputGroup" v-model="items.name" size='small' v-on:change="inputchange">
          <el-option v-for="item in items.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <span class="Embellish"><a href="#" @click=" excellCsv()">下载</a></span>
        <span class="Embellish"><a @click.prevent="loadPicture(Table.tableData)" >图片</a></span>
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
        <el-table class="tablelist" v-loading="loading" :data="Table.tableData_prepag" style="width:100%;position:relative;" :height="Table.height"
          @cell-click="showPicture">
          <el-table-column prop="热销排名" label="排名" width="50" header-align="center" align="center"></el-table-column>
          <el-table-column :label="Table.tableData_title[0]" header-align="center" align="center" width="80">
            <template scope="scope">
              <a target="_blank" :href="Table.bigPicture" alt=""><img style="height:44px;" :src="scope.row.主图缩略图" alt="店铺图片"></a>
            </template>
          </el-table-column>
          <el-table-column show-overflow-tooltip :label="Table.tableData_title[2]" header-align="center" align="center">
            <template scope="scope"><a target="_blank" :href="scope.row.宝贝链接" alt="">{{scope.row.商品信息}}</a></template>
          </el-table-column>
          <el-table-column show-overflow-tooltip prop="所属店铺" :label="Table.tableData_title[3]" header-align="center" align="center"
            width="150">
            <template scope="scope"><a target="_blank" :href="scope.row.店铺链接">{{scope.row.所属店铺}}</a></template>
          </el-table-column>
          <el-table-column :prop="Table.tableData_title[4]" :label="Table.tableData_title[4]" header-align="right" align="right" width="120"></el-table-column>
          <el-table-column :prop="Table.tableData_title[5]" :label="Table.tableData_title[5]" header-align="right" align="right" width="120">
            <template scope="scope"><span>{{scope.row.交易增长幅度 |number-filter}}</span></template>
          </el-table-column>
          <el-table-column :prop="Table.tableData_title[6]" :label="Table.tableData_title[6]" header-align="right" align="right" width="120"></el-table-column>
            <el-table-column :prop="Table.tableData_title[11]" :label="Table.tableData_title[11]" header-align="right" align="right"
              width="50"></el-table-column>
            <el-table-column :prop="Table.tableData_title[12]" :label="Table.tableData_title[12]" header-align="right" align="right"
              width="50"></el-table-column>
            <el-table-column :prop="Table.tableData_title[13]" :label="Table.tableData_title[13]" header-align="right" align="right"
              width="50"></el-table-column>
            <el-table-column :prop="Table.tableData_title[14]" :label="Table.tableData_title[14]" header-align="right" align="right"
              width="50"></el-table-column>
            <el-table-column :prop="Table.tableData_title[15]" :label="Table.tableData_title[15]" header-align="right" align="right"
              width="50"></el-table-column>
            <el-table-column :prop="Table.tableData_title[16]" :label="Table.tableData_title[16]" header-align="right" align="right"
              width="50"></el-table-column>
            <el-table-column :prop="Table.tableData_title[17]" :label="Table.tableData_title[17]" header-align="right" align="right"
              width="50"></el-table-column>
          <template v-if="Table.tableData_title[18]">
            <el-table-column :prop="Table.tableData_title[18]" :label="Table.tableData_title[18]" header-align="right" align="right"
              width="50"></el-table-column>
            <el-table-column :prop="Table.tableData_title[19]" :label="Table.tableData_title[19]" header-align="right" align="right"
              width="50"></el-table-column>
            <el-table-column :prop="Table.tableData_title[20]" :label="Table.tableData_title[20]" header-align="right" align="right"
              width="50"> </el-table-column>
            <el-table-column :prop="Table.tableData_title[21]" :label="Table.tableData_title[21]" header-align="right" align="right"
              width="50"></el-table-column>
            <el-table-column :prop="Table.tableData_title[22]" :label="Table.tableData_title[22]" header-align="right" align="right"
              width="50"></el-table-column>
            <el-table-column :prop="Table.tableData_title[23]" :label="Table.tableData_title[23]" header-align="right" align="right"
              width="50"></el-table-column>
            <el-table-column :prop="Table.tableData_title[24]" :label="Table.tableData_title[24]" header-align="right" align="right"
              width="50"> </el-table-column>
          </template>
          <el-table-column header-align="center" align="center" label="操作" width="120">
            <template scope="scope"><a target="_blank" :href="scope.row.查看详情" value='' alt=""> 查看详情</a><br>
              <a target="_blank" :href="scope.row.同款货源" alt="">同款货源</a></template>
          </el-table-column>
        </el-table>
        <transition name="page">
          <div v-show='!loading' style="text-align:center;">
            <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="Table.PageIndex" :page-sizes="[15, 25, 50, 100]"
              :page-size="Table.prePageCount" layout="total, sizes, prev, pager, next, jumper" :total="Table.tableData.length"></el-pagination>
          </div>
        </transition>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import {
    mapActions
  } from 'vuex'
  import {
    PICTURE_INSERT
  } from '../../store/picture'
  export default {
    data() {
      return {
        Tvalue: '',
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
        inputGroup: [{
          name: '牛仔裤',
          value: [{
            label: '类目：牛仔裤',
            value: '牛仔裤'
          }, {
            label: '类目：休闲裤',
            value: '休闲裤'
          }, {
            label: '类目：打底裤',
            value: '打底裤'
          }]
        }, {
          name: '热销排名',
          value: [{
            value: '热销排名',
            label: '趋势：热销排名'
          }, {
            value: '支付转化率指数',
            label: '趋势：支付转化率指数'
          }, {
            value: '交易增长幅度',
            label: '趋势：交易增长幅度'
          }, {
            value: '支付子订单数',
            label: '趋势：支付子订单数'
          }]
        }, {
          name: 7,
          value: [{
            value: 7,
            label: '天数：近7天'
          }, {
            value: 14,
            label: '天数：近14天'
          }]
        }],
        Table: {
          tableData: [],
          tableData_title: [],
          tableData_prepag: [],
          prePageCount: 15,
          PageIndex: 1,
          height: 830,
          bigPicture: null
        },
        loading: true,
        restaurants: [],
        value4: '',
        value5: '',
        timeout: null,
        fullpath: ''
      };
    },
    mounted() {
      // 显示遮罩层加载功能
      this.$http.get("prod/hot").then((response) => {
        this.loading = false
        // this.fullpath = response.body.fullpath 
        this.objToArr(response.body.data)
      })
      this.$http.get("shop/search").then((response) => {
        if (response.data) {
          this.restaurants = response.data.map((item) => {
            return {
              value: item
            }
          })
        }
      })
    },
    methods: {
      ...mapActions([PICTURE_INSERT]),
      excellCsv() {
        this.$http.get("prod/hot/download").then((response) => {
          this.fullpath = response.body.fullpath
          
         
            console.log(this)
     
        })
      },
      inputchange() {
        var data1 = {
          "data_time": this.Tvalue,
          "data_items": this.inputGroup[0].name,
          "data_reorder": this.inputGroup[1].name,
          "data_time_length": this.inputGroup[2].name,
          "choice": this.$data.value4,
          "titlechoice": this.$data.value5

        }
        var data = JSON.stringify(data1) //格式化数据
        this.loading = true
        this.$http.post("prod/hot", {
          data
        }, {
          emulateJSON: true
        }).then((response) => {
          this.fullpath = response.body.fullpath
          this.objToArr(response.body.data)
          this.loading = false
        })
      },
      objToArr(obj) {
        var middle_Table_body = [];
        var middle_Table_title = [];
        if (obj) {
          if (this.inputGroup[1].name == "交易增长幅度") {
            for (let i in obj) {
              let Itme = {}
              for (let j in obj[i]) {
                if (j.slice(0, 2) == "日期") {
                  let Itme_key = j.split('：')[1].substring(4, 6) + '-' + j.split('：')[1].substring(6, 8)
                  Itme[Itme_key] = parseFloat(obj[i][j] * 100).toFixed(2) + '%'
                } else {
                  Itme[j] = obj[i][j]
                }
              }
              middle_Table_body.push(Itme)
            }
          } else {
            for (let i in obj) {
              let Itme = {}
              for (let j in obj[i]) {
                if (j.slice(0, 2) == "日期") {
                  let Itme_key = j.split('：')[1].substring(4, 6) + '-' + j.split('：')[1].substring(6, 8)
                  Itme[Itme_key] = obj[i][j]
                } else {
                  Itme[j] = obj[i][j]
                }
              }
              middle_Table_body.push(Itme)
            }
          }
          for (var j in middle_Table_body[0]) {
            middle_Table_title.push(j)
          }
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
      showPicture(row, cell) {
        if (cell.label == "主图缩略图") {
          this.Table.bigPicture = row.主图缩略图.slice(0, -10)
        }
      },
      querySearchAsync(queryString, cb) {
        var restaurants = this.restaurants
        var results = queryString ? restaurants.filter(this.createStateFilter(queryString)) : restaurants;
        clearTimeout(this.timeout);
        this.timeout = setTimeout(() => {
          cb(results);
        });
      },
      createStateFilter(queryString) {
        return (state) => {
          return (state.value.indexOf(queryString.toLowerCase()) === 0);
        }
      },
      emptyFilter() {
        this.value4 = ''
        this.value5 = ''
        this.inputchange()
      },
      loadPicture(data) {
        this.PICTURE_INSERT(data) //数据存入store,详情请见
        window.router.push({
          path: '/picture/download/'
        })
      }
    }
  }

</script>
