<template>
  <div>
    <el-row class="title" type="flex" justify="space-between" align="middle">
      <el-col class="title-left">
        <h3>趋势分布</h3>
      </el-col>
      <el-col class="title-right">
        <p>属性成交趋势</p>
      </el-col>
    </el-row>
    <el-row class="navlist" type="flex" justify="space-around" align="middle">
      <el-col class="list-left">
        <el-select v-model.lazy="value0" size='mini' v-on:change="InputCategory" placeholder="选择类目">
          <el-option v-for="item in options0" v-once :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-select v-model.lazy="value1" size='mini' v-on:change="InputAttribute" placeholder="选择属性分类">
          <el-option v-for="item in options1" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-select v-model.lazy="value2" size='mini' placeholder="选择属性">
          <el-option v-for="item in options2" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-select v-model.lazy="value3" size='mini' v-on:change="InputFeature" placeholder="选取行业属性">
          <el-option v-for="item in options3" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-col>
    </el-row>
    <el-row  v-show="show" style="backgroundColor:#F9FAFC;height:100%;">
      <el-col v-loading="loading" style="width:98%;height:780px;margin:1%;backgroundColor:#FFF;">
        <IEcharts style="width:100%;height:100%;" :option="option" :resizable="true"></IEcharts>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  import IEcharts from 'vue-echarts-v3/src/full.vue';
  import 'echarts/lib/chart/line';
  export default {
    components: {
      IEcharts
    },
    data() {
      return {
        show:false,
        loading:false,
        value0: '',
        options0: [{
          label: '牛仔裤',
          value: '牛仔裤'
        }, {
          label: '休闲裤',
          value: '休闲裤'
        }, {
          label: '打底裤',
          value: '打底裤'
        }, {
          label: '半身裙',
          value: '半身裙'
        }, {
          label: '大码女装',
          value: '大码女装'
        }, {
          label: '连衣裙',
          value: '连衣裙'
        }, {
          label: '棉裤羽绒裤',
          value: '棉裤羽绒裤'
        }, {
          label: '西装裤正装裤',
          value: '西装裤正装裤'
        }, {
          label: '成交量分布',
          value: '成交量分布'
        }],
        value1: '',
        options1: [],
        value2: '',
        options2: [],
        value3: '',
        options3: [{
          label: "成交量",
          value: "成交量"
        }, {
          label: "销售额",
          value: "销售额"
        }, {
          label: "高质宝贝数",
          value: "高质宝贝数"
        }],
        option: {
          color:['#F20030','#FFF200','#2BD4FF'],
          title: {
            text: '类目属性关系图',
            subtext: '数据来自生e经',
            x: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer:{
              type:'cross'
            },
            formatter:function(params){
              var res = params[0].name;
              res+='<br/>'+params[0].seriesName+':'+params[0].value;
              res+='<br/>'+params[1].seriesName+':'+params[1].value;
              res+='<br/>'+params[2].seriesName+':'+(params[2].value*100).toFixed(2);
              return res
            }
          },
          legend: {
            data: [],
            right: 50
          },
          axisPointer: {
            link: {
              xAxisIndex: 'all'
            }
          },
          dataZoom: [{
             type: 'slider',
              show: true,
              realtime: true,
              start: 50,
              end: 100,
              labelPrecision: 2,
              xAxisIndex: [0, 1,2]
            },
            {
              type: 'inside',
              realtime: true,
              start: 50,
              end: 100,
              xAxisIndex: [0, 1,2]
            }
          ],
          grid: [{
            left: 60,
            right: 50,
            height: '23%'
          }, {
            left: 60,
            right: 50,
            top: '38%',
            height: '23%',
          }, {
            left: 60,
            right: 50,
            top: '68%',
            height: '23%',
          }],
          xAxis: [{
             gridIndex: 0,
              type: 'category',
              boundaryGap: false,
              axisLine: {
                onZero: true
              },
              data: []
            },
            {
              gridIndex: 1,
              type: 'category',
              boundaryGap: false,
              axisLine: {
                onZero: true
              },
              data: []
            },
            {
              gridIndex: 2,
              type: 'category',
              boundaryGap: false,
              axisLine: {
                onZero: true
              },
              data: []
            }
          ],
          yAxis: [{
              name: '',
              nameGap:6,
              type: 'value',
              nameTextStyle:{
                fontWeight:'bold',
                fontSize:14
              },
              axisLabel: {
                formatter: function (val) {
                    return (val/10000) + '万';
                }
            }
            },
            {
              gridIndex: 1,
              name: '',
              nameGap:6,
              type: 'value',
               nameTextStyle:{
                fontWeight:'bold',
                fontSize:14
              },
               axisLabel: {
                formatter: function (val) {
                    return (val/10000) + '万';
                }
            }
            },
             {
              gridIndex: 2,
              name: '',
              nameGap:6,
              type: 'value',
               nameTextStyle:{
                fontWeight:'bold',
                fontSize:14
              },
              axisLabel: {
                formatter: function (val) {
                    return (val* 100).toFixed(1) + '%'
            }
            }
             }],
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
        }
      }
    },
    methods: {
      InputCategory() { //类目输入时后两项清空原属性
        this.loading=true
        this.options1.splice(0, this.options1.length)
        this.options2.splice(0, this.options1.length)
        this.loading=true
        var data= {
          category: this.value0,
          attribute: 'list'
        }
        this.$http.post('proper/trend', {
          data
        }, {
          emulateJSON: true
        }).then((response) => {
          this.options1 = Object.keys(response.body.data).map(function (item) {
            return {
              label: response.body.data[item],
              value: response.body.data[item]
            }
          })
          this.loading=false
        })
      },
      InputAttribute() { //属性输入时前父选项不变,子选项清空
    
        this.options2 = []
        var data = this.data
        this.loading=true
        var data= {
          category: this.value0,
          attribute: this.value1,
          feature: 'list'
        }
        this.$http.post('proper/trend', {
          data
        }, {
          emulateJSON: true
        }).then((response) => {
          this.options2 = Object.keys(response.body.data).map(function (item) {
            return {
              label: response.body.data[item],
              value: response.body.data[item]
            }
          })
          this.loading=false
        })
      },
      InputFeature() {
        this.loading=true
        var data= {
          category: this.value0,
          attribute: this.value1,
          feature: this.value2,
          variable: this.value3
        }
        this.$http.post('proper/trend', {
          data
        }, {
          emulateJSON: true
        }).then((response) => {
          this.option.xAxis[0].data= this.option.xAxis[1].data=this.option.xAxis[2].data = Object.keys(response.body.data1).map(function (item) {
            var data = new Date(response.body.data1[item]['日期'])
            return [data.getFullYear(), data.getMonth() + 1].join('-')
          })
          var _this=this
           this.option.series[0].data= Object.keys(response.body.data0).map(function (item) {
            return response.body.data0[item][_this.value3]
          })
           this.option.series[0].name=this.option.yAxis[0].name=this.value1
          this.option.series[1].data=Object.keys(response.body.data1).map(function (item) {
            return response.body.data1[item][_this.value3]
          })
           this.option.series[1].name=this.option.yAxis[1].name=this.value2
           this.option.series[2].data = Object.keys(response.body.data2).map(function (item) {
            return response.body.data2[item][_this.value3]
          })
            this.option.series[2].name=this.option.yAxis[2].name='占比'
             this.option.legend.data=[this.value1,this.value2,'占比']
             this.show=true
             this.loading=false     
        })
      }
    }
}
</script>
<style>
  .navlist .small {
    width: 15%;
    padding-left: 1%;
    height: 90%;
    padding-top: 10px;
  }

  .navlist .small-group {
    width: 50%;
    position: absolute;
    right: 2%;
    background-color: #E5E9F2;
    top: 4px;
    height: 80%;
    border: 1px solid #C0CCDA;
    border-radius: 4px;
    padding-left: 4px;
    display: inline-block;
    cursor: Pointer;
    font-size: 14px;
  }

  .navlist .small-group div {
    position: absolute;
    display: inline-block;
    left: -10%;
    top: 10px;
    font-size: 16px;
  }

</style>
