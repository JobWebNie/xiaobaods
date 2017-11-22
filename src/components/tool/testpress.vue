<style scoped>
  .time-line-horizon {
    position: relative;
    top: 100px;
  }

</style>
<template>
  <div>
    <el-row class="title" type="flex" justify="space-between" align="middle">
      <el-col class="title-left">
        <h3>计算器</h3>
      </el-col>
    </el-row>
    <el-col :span="4" :push="1">
      <b> 选择：</b>
      <el-radio-group v-model="slename" @change="changename">
        <el-radio label="牛仔裤">牛仔裤</el-radio>
        <el-radio label="打底裤">打底裤</el-radio>
      </el-radio-group>
      <br>
      <b> 输入</b>
      <el-input v-model="input" placeholder="请输入内容"></el-input>
      <div>
        <b>结果：</b>{{result}}</div>
    </el-col>
    <div class="time-line-horizon" v-for="item in picture">
      <div class="el-steps is-horizontal">
        <div class="el-step is-horizontal" style="width: 200px; margin-right: 0px;">
          <div class="el-step__head is-finish is-text">
            <div class="el-step__line is-horizontal" style="margin-right: 0px;">
              <i class="el-step__line-inner" style="transition-delay: 0ms; border-width: 1px; width: 50%;"></i>
            </div>
            <span class="el-step__icon">
              <div>1</div>
            </span>
          </div>
          <div class="el-step__main" style="margin-left: 0px;">
            <div class="el-step__title is-finish">{{item.title}}</div>
            <div class="el-step__description is-finish">{{item.path}}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        picture:[{'title':'标题一',path:'//image.jpg'},{'title':'标题二',path:'//image.jpg'}],
        slename: '牛仔裤',
        input: 0,
        result: null,
        m: null,
        n: null,
        b: null,

      }
    },
    watch: {
      input: function (val, oldVal) {
        this.result = this.m * val + this.n * val * val + this.b
      }
    },
    mounted() {
      this.changename()
    },
    methods: {
      changename() {

        this.$http.post('conversion/parms', {
          name: this.slename
        }, {
          emulateJSON: true
        }).then((response) => {
          this.m = response.data.coef_0
          this.n = response.data.coef_1
          this.b = response.data.intercept
          this.result = this.m * this.input + this.n * this.input * this.input + this.b
        })
      }

    }
  }

</script>

<!--
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

  .step {
    height: 150px;
  }

</style>
<template>
  <div>
    <div class="mylove">
      <el-row :gutter="20">
        <el-col>
          <el-input size="small" v-model="input" class="myloin" placeholder="搜索商品" icon="search"></el-input>
        </el-col>
      </el-row>
    </div>
    <div class="chart">
      <IEcharts :option="option_data"></IEcharts>
    </div>
    <div class="step">
      <el-popover ref="popover" placement="right" width="400" trigger="hover">
        <div v-for="item in picture_change_date">
            <h3>{{item.date}}<br/>{{item.description}}</h3>
            <img v-if="item.path" :src="item.path" alt="">
            <p>{{item.keyworlds}}</p>
        </div>
      </el-popover>
      <el-button v-popover:popover style="position:relative;">1</el-button>
    </div>

  </div>
</template>
<script>
  import IEcharts from 'vue-echarts-v3/src/full.vue';
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
            text: '类目属性关系图',
            subtext: '数据来自生e经',
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
            data: ['支付子订单数', '交易增长幅度', '支付转化率指数'],
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
              name: '支付子订单数',
              type: 'line',
              smooth: true,
              symbolSize: 8,
              hoverAnimation: false,
              data: []
            },
            {
              name: '交易增长幅度',
              type: 'line',
              smooth: true,
              xAxisIndex: 1,
              yAxisIndex: 1,
              symbolSize: 8,
              hoverAnimation: false,
              data: []
            },
            {
              name: '支付转化率指数',
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
      this.$http.get('prod/hotid').then((response) => {
        var data_reciver = response.body.data
        Object.keys(data_reciver).map((index) => {
          let datecategray = this.date_format_from_millisecond(data_reciver[index]['日期'], 'YYYY-MM-dd')
          this.option_data.xAxis[0].data.push(datecategray)
          this.option_data.xAxis[1].data.push(datecategray)
          this.option_data.xAxis[2].data.push(datecategray)
          this.option_data.series[0].data.push(data_reciver[index]['支付子订单数'])
          this.option_data.series[1].data.push(data_reciver[index]['交易增长幅度'])
          this.option_data.series[2].data.push(data_reciver[index]['支付转化率指数'])
        })
        this.picture_change_date = this.find_change_picture_or_information(data_reciver)
      })
    },
    methods: {
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
          } else {
            return
          }
        })
        return pictures
      },
      doclick() {
        console.log('click')
      }
    }
  }

</script>
-->
