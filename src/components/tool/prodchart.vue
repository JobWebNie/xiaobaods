<style>
  .chart {
    height: 500px;
    width: 1500px;
  }

  .mylove {
    height: 70px;
    width: 100%;
    box-shadow: 0 0 3px #222;
  }

  .mylove .myloin {
    margin: 5px;
    width: 120px;
  }

  .mystep {
    margin-left:20px;
    height:calc(100vh - 570px);
    overflow:auto;
  }

</style>
<template>
  <div>
    <div class="mylove">
      <el-row :gutter="20">
        <el-col>
          <el-input size="small" v-model="input" class="myloin" placeholder="搜索商品" icon="search" :on-icon-click="search_product_from_id"></el-input>
        </el-col>
      </el-row>
    </div>
    <div class="chart">
      <IEcharts :option="option_data"></IEcharts>
    </div>
    <div class="el-steps is-horizontal mystep">
      <div class="el-step is-horizontal" v-for="(item,key) in picture_change_date" style="width: 300px; margin-right: 0px;">
        <div class="el-step__head is-wait is-text">
          <div class="el-step__line is-horizontal" style="margin-right: 0px;">
            <i class="el-step__line-inner" style="transition-delay: 0ms; border-width: 1px; width: 50%;"></i>
          </div>
          <span class="el-step__icon">
            <div>{{key}}</div>
          </span>
        </div>
        <div class="el-step__main" style="margin-left:10px;position:relative;">
          
          <div class="el-step__title" style="position:absolute;">
          <h3 style="margin-bottom:0px;">{{item.date}}</h3><div>{{key==0 ?'':item.description}}</div>
          <span style="pddding:4px;">
            <img v-if="item.path" :src="item.path.slice(0,-10)" alt="" style="width:60%;">
          </span>
            <p class="el-step__description">{{item.keyworlds}}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import IEcharts from 'vue-echarts-v3/src/full.vue';
  import { mapState ,mapActions} from 'vuex'
  export default {
    components: {
      IEcharts
    },
    data() {
      return {
        input: '',
        option_data: {
          color: ['#F20030', '#FFF200', '#2BD4FF'],
          title: {
            text: '商品变化历程',
            subtext: '主图、关键词',
            x: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross'
            },
            formatter: function (params) {
              var res = params[0].name;
              res += '<br/>' + params[0].seriesName + ':' + params[0].value;
              res += '<br/>' + params[1].seriesName + ':' + (params[1].value * 100).toFixed(2);
              res += '%<br/>' + params[2].seriesName + ':' + params[2].value;
              return res
            }
          },
          legend: {
            data: [],
            right: 50
          },
          grid: [{
            left: 60,
            right: 50,
          }, {
            left: 60,
            right: 50,
          }, {
            left: 60,
            right: 50,

          }],
          xAxis: [{
              gridIndex: 0,
              type: 'category',
              boundaryGap: false,
              axisLine: {
                onZero: false
              },
              data: []
            },
            {
              show: false,
              gridIndex: 1,
              type: 'category',
              boundaryGap: false,
              axisLine: {
                onZero: false
              },
              data: []
            },
            {
              show: false,
              gridIndex: 2,
              type: 'category',
              boundaryGap: false,
              axisLine: {
                onZero: false
              },
              data: []
            }
          ],
          yAxis: [{
              show: false,
              type: 'value'
            },
            {
              offset: -50,
              show: false,
              gridIndex: 1,
              type: 'value'
            },
            {
              show: false,
              offset: -100,
              gridIndex: 2,
              type: 'value'
            }
          ],
          series: [{
              name: '',
              type: 'line',
              smooth: true,
              symbolSize: 8,
              hoverAnimation: false,
              data: []
            },
            {
              name: '',
              type: 'line',
              smooth: true,
              xAxisIndex: 1,
              yAxisIndex: 1,
              symbolSize: 8,
              hoverAnimation: false,
              data: []
            },
            {
              name: '',
              type: 'line',
              smooth: true,
              xAxisIndex: 2,
              yAxisIndex: 2,
              symbolSize: 8,
              hoverAnimation: false,
              data: []
            }
          ]
        },
        picture_change_date: []
      }
    },
    created() {
      var options = this.$store.state.prodId
      this.search_product_from_id(options)
    },
    beforeDestroy(){
     sessionStorage.setItem('prodId',this.$store.state.prodId)
    },
    methods: {
       ...mapActions(['PRODUCT_SEARCH']),
      date_format_from_millisecond(millisecond, formatStr) {
        if (typeof millisecond == 'number') {
          var _this = new Date(millisecond)
          var str = formatStr;
          var Week = ['日', '一', '二', '三', '四', '五', '六'];
          str = str.replace(/yyyy|YYYY/, _this.getFullYear());
          str = str.replace(/yy|YY/, (_this.getYear() % 100) > 9 ? (_this.getYear() % 100).toString() : '0' + (_this.getYear() %
            100));
          str = str.replace(/MM/, (_this.getMonth() + 1) > 9 ? (_this.getMonth() + 1).toString() : '0' + (_this.getMonth() +
            1));
          str = str.replace(/M/g, (_this.getMonth() + 1));
          str = str.replace(/w|W/g, Week[_this.getDay()]);
          str = str.replace(/dd|DD/, _this.getDate() > 9 ? _this.getDate().toString() : '0' + _this.getDate());
          str = str.replace(/d|D/g, _this.getDate());
          str = str.replace(/hh|HH/, _this.getHours() > 9 ? _this.getHours().toString() : '0' + _this.getHours());
          str = str.replace(/h|H/g, _this.getHours());
          str = str.replace(/mm/, _this.getMinutes() > 9 ? _this.getMinutes().toString() : '0' + _this.getMinutes());
          str = str.replace(/m/g, _this.getMinutes());
          str = str.replace(/ss|SS/, _this.getSeconds() > 9 ? _this.getSeconds().toString() : '0' + _this.getSeconds());
          str = str.replace(/s|S/g, _this.getSeconds());
          return str;
        }
      },
      find_change_picture_or_information(some_data) {
        var pictures = []
        Object.keys(some_data).map((index) => {
          var date = this.date_format_from_millisecond(some_data[index]['日期'], 'YYYY-MM-DD')
          if (some_data[index]['主图缩略图'] !== '-' && some_data[index]['商品信息'] !== '-') {
            pictures.push({
              'date': date,
              'description': '关键词、主图都改变',
              'path': some_data[index]['主图缩略图'],
              'keyworlds': some_data[index]['商品信息']
            })
          } else if (some_data[index]['主图缩略图'] !== '-' && some_data[index]['商品信息'] == '-') {
            pictures.push({
              'date': date,
              'description': '主图变更',
              'path': some_data[index]['主图缩略图']
            })
          } else if (some_data[index]['主图缩略图'] == '-' && some_data[index]['商品信息'] !== '-') {
            pictures.push({
              'date': date,
              'description': '关键词变更',
              'keyworlds': some_data[index]['商品信息']
            })
          } else {;
          }
        })
        return pictures
      },
      search_product_from_id(options) {
        this.$http.get('prod/hotid', {
          params: options
        }).then((response) => {
          var data_reciver = response.body
          
          if (data_reciver.code == 200) {
            if(this.$store.state.prodId.table == 'bc_attribute_granularity_sales'){
              Object.keys(data_reciver.data).map((index) => {
              let datecategray = this.date_format_from_millisecond(data_reciver.data[index]['日期'], 'YYYY-MM-dd')
              this.option_data.xAxis[0].data.push(datecategray)
              this.option_data.xAxis[1].data.push(datecategray)
              this.option_data.xAxis[2].data.push(datecategray)
              this.option_data.legend.data=['支付子订单数','交易增长幅度','支付转化率指数']
              this.option_data.series[0].name= this.option_data.legend.data[0]
              this.option_data.series[1].name= this.option_data.legend.data[1]
              this.option_data.series[2].name= this.option_data.legend.data[2]
              this.option_data.series[0].data.push(data_reciver.data[index]['支付子订单数'])
              this.option_data.series[1].data.push(data_reciver.data[index]['交易增长幅度'])
              this.option_data.series[2].data.push(data_reciver.data[index]['支付转化率指数'])
            })
            }else if(this.$store.state.prodId.table == 'bc_attribute_granularity_visitor'){
              Object.keys(data_reciver.data).map((index) => {
              let datecategray = this.date_format_from_millisecond(data_reciver.data[index]['日期'], 'YYYY-MM-dd')
              this.option_data.xAxis[0].data.push(datecategray)
              this.option_data.xAxis[1].data.push(datecategray)
              this.option_data.xAxis[2].data.push(datecategray)
              this.option_data.legend.data=['流量指数','搜索人气','支付子订单数']
              this.option_data.series[0].name= this.option_data.legend.data[0]
              this.option_data.series[1].name= this.option_data.legend.data[1]
              this.option_data.series[2].name= this.option_data.legend.data[2]
              this.option_data.series[0].data.push(data_reciver.data[index]['流量指数'])			
              this.option_data.series[1].data.push(data_reciver.data[index]['搜索人气'])
              this.option_data.series[2].data.push(data_reciver.data[index]['支付子订单数'])
            })
            }else{
              Object.keys(data_reciver.data).map((index) => {
              let datecategray = this.date_format_from_millisecond(data_reciver.data[index]['日期'], 'YYYY-MM-dd')
              this.option_data.xAxis[0].data.push(datecategray)
              this.option_data.xAxis[1].data.push(datecategray)
              this.option_data.xAxis[2].data.push(datecategray)
              this.option_data.legend.data=['支付转化率指数','支付件数','支付子订单数']
              this.option_data.series[0].name= this.option_data.legend.data[0]
              this.option_data.series[1].name= this.option_data.legend.data[1]
              this.option_data.series[2].name= this.option_data.legend.data[2]
              this.option_data.series[0].data.push(data_reciver.data[index]['支付转化率指数'])					
              this.option_data.series[1].data.push(data_reciver.data[index]['支付件数'])
              this.option_data.series[2].data.push(data_reciver.data[index]['支付子订单数'])
            })
            }
       
            this.picture_change_date = this.find_change_picture_or_information(data_reciver.data)
     
          }
        })
      }
    }
  }

</script>
