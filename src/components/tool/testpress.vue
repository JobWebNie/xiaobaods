<!--<template>
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
      <el-row>
   
      </el-row>
    </el-col>

  </div>
</template>
<script>
  export default {
    data() {
      return {
        
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
-->

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
    margin-top:5px;
    width: 100px;
  }

  .bg-purple {
    color: #324057;
    box-shadow: 0 2px 0 0 #34C0E3;
    text-align: center;
    border-radius: 2px;
  }

</style>
<template>
  <div>
    <div>
      <!--<div>
        <el-row class="title" type="flex" justify="space-between" align="middle">
          <el-col class="title-left">
            <h3>热销产品趋势分析</h3>
          </el-col>
          <el-col class="title-right">
            <p>针对特定节点和分类，对一定时间周期内排名，订单数进行追踪</p>
          </el-col>
        </el-row>
        <el-input class="myinput" v-model="input" placeholder="搜索商品" icon="search"></el-input>
      </div>-->
      <div class="mylove">
        <el-row :gutter="20">
          <el-col :span="1">
            <div class="bg-purple">排名</div>
          </el-col>
          <el-col :span="2">
            <div class="bg-purple"> 商品信息</div>
          </el-col>
          <el-col :span="2">
            <div class="bg-purple"> 流量指数 </div>
          </el-col>
          <el-col >
            <el-input size="small" v-model="input" class="myloin"></el-input>
            
          </el-col>
        </el-row>
      </div>
    </div>
    <div class="chart">
      <IEcharts :option="option"></IEcharts>
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
        option: {
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
              res += '<br/>' + params[1].seriesName + ':' + params[1].value;
              res += '<br/>' + params[2].seriesName + ':' + (params[2].value * 100).toFixed(2);
              return res
            }
          },
          legend: {
            data: ['第一', '第二', '第三'],
            right: 50
          },
          axisPointer: {
            link: {
              xAxisIndex: 'all'
            }
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
                onZero: true
              },
              data: ["2015-1", "2015-2", "2015-3", "2015-4", "2015-5", "2015-6", "2015-7", "2015-8", "2015-9",
                "2015-10", "2015-11", "2015-12"
              ]
            },
            {
              gridIndex: 1,
              type: 'category',
              boundaryGap: false,
              axisLine: {
                onZero: true
              },
              data: ["2015-1", "2015-2", "2015-3", "2015-4", "2015-5", "2015-6", "2015-7", "2015-8", "2015-9",
                "2015-10", "2015-11", "2015-12"
              ]
            },
            {
              gridIndex: 2,
              type: 'category',
              boundaryGap: false,
              axisLine: {
                onZero: true
              },
              data: ["2015-1", "2015-2", "2015-3", "2015-4", "2015-5", "2015-6", "2015-7", "2015-8", "2015-9",
                "2015-10", "2015-11", "2015-12"
              ]
            }
          ],
          yAxis: [{
              show: false,
              type: 'value'
            },
            {
              show: false,
              gridIndex: 1,
              type: 'value'
            },
            {
              show: false,
              gridIndex: 2,
              type: 'value'
            }
          ],
          series: [{
              name: '第一',
              type: 'line',
              smooth: true,
              symbolSize: 8,
              hoverAnimation: false,
              data: [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
            },
            {
              name: '第二',
              type: 'line',
              smooth: true,
              xAxisIndex: 1,
              yAxisIndex: 1,
              symbolSize: 8,
              hoverAnimation: false,
              data: [3.9, 5.9, 11.1, 18.7, 48.3, 69.2, 231.6, 46.6, 55.4, 18.4, 10.3, 0.7]
            },
            {
              name: '第三',
              type: 'line',
              smooth: true,
              xAxisIndex: 2,
              yAxisIndex: 2,
              symbolSize: 8,
              hoverAnimation: false,
              data: [6.9, 7.9, 15.1, 19.7, 51.3, 73.2, 245.6, 50.6, 63.4, 21.4, 11.3, 2]
            }
          ]
        }
      }
    },
    created(){
      this.$http.get('prod/hotid').then((response)=>{
        console.log(response.body.data)
      })
    },
    methods: {

    }
  }

</script>
