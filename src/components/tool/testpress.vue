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


<!--<template>
  <div>
    <div>
      <el-select v-model="value5" placeholder="请选择">
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
        </el-option>
      </el-select>
    </div>
    <div class="echarts">
      <IEcharts :option="bar" @ready="onReady" @click="onClick"></IEcharts>
      <button @click="doRandom">Random</button>
    </div>
  </div>
</template>
<script>
  import IEcharts from 'vue-echarts-v3/src/full.vue';

var weatherIcons = {
    'Sunny': 'http://echarts.baidu.com/images/logo.png',
    'Cloudy': 'http://echarts.baidu.com/images/logo.png',
    'Showers': 'http://echarts.baidu.com/images/logo.png'
};
  export default {
    name: 'view',
    components: {
      IEcharts
    },
    props: {},
    data: () => ({
        options: [{
          value: '选项1',
          label: '黄金糕'
        }, {
          value: '选项2',
          label: '双皮奶'
        }, {
          value: '选项3',
          label: '蚵仔煎'
        }, {
          value: '选项4',
          label: '龙须面'
        }, {
          value: '选项5',
          label: '北京烤鸭'
        }],
        value5: '',
        loading: true,
        bar: {
          title: {
            text: '商品近期表现',
            subtext: '数据真实'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['交易增长幅度', '支付子订单数', '支付转化率指数']
          },
          toolbox: {
            show: true,
            feature: {
              magicType: {
                show: true,
                type: ['stack', 'tiled']
              },
              saveAsImage: {
                show: true
              }
            }
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            axisLabel:{
            formatter: function (value) {
                return '{value|' + value + '}\n{' + value + '| }';
            },
            rich:{
                Sunny: {
                    align: 'center'
                },
                Cloudy: {
                    align: 'right'
                },
                Showers: {
                    align: 'right'
                
                }
              }
            },
            data: ['Sunny', 'Cloudy', 'Showers','Sun', 'Clou', 'Shows','valj'],
          },
          yAxis: [{
            show:false,
            type: 'value'
          },{
             show:false,
              type: 'value'
          },{
             show:false,
              type: 'value'
          }],
          series: [{
              name: '支付转化率指数',
              type: 'line', 
              symbol:'circle',
              smooth: true,
              data: [160,166,159,160,156,140,140]
            },
            {
              name: '支付子订单数',
              type: 'line',
               symbol:'circle',
              yAxisIndex: 1,
              smooth: true,
              data: [140,1736,1696,1627,1573,1480,1680,1680]
            },
            {
              name: '交易增长幅度',
              type: 'line',
               symbol:'circle',
              yAxisIndex: 2,
              smooth: true,
              data: [-0.03,-0.02,-0.05,-0.03,-0.04,0.13,0.13]
            }
          ]
        }
    }),
  methods: {
    doRandom() {
      const that = this;
      let data = [];
      for (let i = 0, min = 5, max = 99; i < 6; i++) {
        data.push(Math.floor(Math.random() * (max + 1 - min) + min));
      }
      that.loading = !that.loading;
      that.bar.series[0].data = data;
    },
    onReady(instance) {
      console.log(instance);
    },
    onClick(event, instance, echarts) {
      console.log(arguments);
    }
  }
  };

</script>

<style scoped>
  .echarts {
    width: 900px;
    height: 300px;
  }

</style>-->
<template>

  <CommitChart :data="data" :options="options" style="width:400px;height:400px;"></CommitChart>
</template>
<script>
  import CommitChart from './CommitChart.js'

  export default {
    components: {
      CommitChart
    },
    data() {
      return {
        data: {
          labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
          datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
              'rgba(196, 88, 186, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
              'rgba(196, 88, 186,1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true
              }
            }]
          }
        }
      }
    },
    mounted() {
      // Overwriting base render method with actual data.

    }
  }

</script>
