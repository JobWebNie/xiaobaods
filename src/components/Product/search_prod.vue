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
        <el-select  v-model="data.category" size='small' v-on:change="inputchange">
          <el-option v-for="item in categoryOption" :label="item.label" :value="item.value"></el-option>
        </el-select>
         <el-select  v-model="data.variable" size='small' v-on:change="inputchange">
          <el-option v-for="item in variableOption" :label="item.label" :value="item.value"></el-option>
        </el-select>
         <el-select  v-model="data.length" size='small' v-on:change="inputchange">
          <el-option v-for="item in lengthOption" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <span class="Embellish"><a @click="excellCsv()">下载</a></span>
        <span class="Embellish"><a @click.prevent="loadPicture()" >图片</a></span>
      </el-col>
      <el-col class="list-right">
        <el-input size='small' @keyup.enter.native="inputchange" v-model.trim="data.titler" placeholder="商品筛选"></el-input>
        <el-input size='small' @keyup.enter.native="inputchange" v-model.trim="data.storer" placeholder="店铺搜索"></el-input>
        <el-autocomplete size='small' v-model="data.storegroupchoice" :fetch-suggestions="querySearchAsync" @keyup.enter.native="inputchange" placeholder="热门店铺分类"></el-autocomplete>
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
          <el-table-column :prop="Table.tableData_title[4]" :label="Table.tableData_title[4]" :formatter="contentFormatter" header-align="right"
            align="right" width="120"></el-table-column>
          <el-table-column :prop="Table.tableData_title[5]" :label="Table.tableData_title[5]" :formatter="contentFormatter" header-align="right"
            align="right" width="120"></el-table-column>
          <el-table-column :prop="Table.tableData_title[6]" :label="Table.tableData_title[6]" :formatter="contentFormatter" header-align="right"
            align="right" width="120"></el-table-column>
          <el-table-column v-for="(title,id) in Table.tableData_title" v-if="title.slice(0,2)=='日期'" :prop="title" :render-header="renderHeader"
            :formatter="contentFormatter" align="right" header-align="right" width="50"></el-table-column>
          <el-table-column header-align="center" align="center" label="操作" width="120">
            <template scope="scope"><a target="_blank" :href="scope.row.查看详情" value='' alt=""> 查看详情</a><br>
              <a target="_blank" :href="scope.row.同款货源" alt="">同款货源</a></template>
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
        // Tvalue: Date.now()- 8.64e7,
        pickerOption: {
          disabledDate(time) {
            var min = Date.parse('2016-11-24')
            var max = Date.now()- 8.64e7;
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
          variableOption:  [{
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
          height: 830,
          bigPicture: null,
          total:null
        },
        data:{
            fun:'a',
            date:Date.now()- 8.64e7,
            length:  7,
            category: '牛仔裤',
            variable: '热销排名',
            storegroupchoice: '',
            storer:'',
            titler: '',
            line_f:0,
            line_b:20, 
            table: 'bc_attribute_granularity_visitor'
        },
        loading: true,
        restaurants: [],
        timeout: null,
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
       this.$http.get("shop/search").then((response) => {
        this.restaurants = response.data.map((item) => {
          return {
            value: item
          }
        })
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
        let reg = String(cellValue).replace(/(\d)(?=(?:\d{3})+$)/g, '$1,')
        let percent = Math.round(cellValue * 100) + '%'
        if (column.property.slice(0, 2) == "日期") {
          const fm = this.data.variable
          switch (fm) {
            case '支付子订单数':
              return cellValue = reg;
              break;
            case '交易增长幅度':
              return cellValue = percent;
              break;
            case '支付转化率指数':
              return cellValue = reg;
              break;
            default:
              return cellValue = cellValue;
              break;
          }
        } else {
          switch (column.property) {
            case '支付子订单数':
              return cellValue = reg;
              break;
            case '交易增长幅度':
              return cellValue = percent;
              break;
            case '支付转化率指数':
              return cellValue = reg;
              break;
            default:
              return cellValue = cellValue;
              break;
          }
        }
      },
      inputchange() {   
        this.loading=true
        var data = JSON.stringify(this.data)
        this.$http.post("prod/search", {data},{emulateJSON:true}).then((response) => {
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
               for(let k in obj[j]){
                 if(k=='total'){
                   this.Table.total=obj[j][k]
                 }else{
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
         this.data.line_b=(this.Table.PageIndex - 1) * val
        this.data.line_f=this.Table.PageIndex * val
        // console.log(this.data)
        this.inputchange()
        // var start = (this.Table.PageIndex - 1) * val //数据起始位置
        // var end = this.Table.PageIndex * val //数据末端位置
        // this.Table.tableData_prepag = this.Table.tableData.slice(start, end) //返回数据
        // this.Table.prePageCount = val
      },
      handleCurrentChange(val) {
        // console.log(`当前页: ${val}`);
        this.Table.PageIndex = val
        this.data.line_b=this.Table.prePageCount * (val - 1)
        this.data.line_f=this.Table.prePageCount * val
        this.inputchange()
        // var start = this.Table.prePageCount * (val - 1) //数据起始位置
        // var end = (this.Table.prePageCount) * val //数据末端位置
        // this.Table.tableData_prepag = this.Table.tableData.slice(start, end) //返回数据
        // this.Table.PageIndex = val
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
        this.data.storegroupchoice = ''
        this.data.storer =''
        this.data.titler = ''
        this.inputchange()
      },
      loadPicture() {
        this.PICTURE_INSERT(this.Table.tableData_prepag) //数据存入store,详情请见
        window.router.push({
          path: '/picture/download/'
        })
      }
    }
  }

</script>
