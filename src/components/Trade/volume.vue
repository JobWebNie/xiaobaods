<template>
  <div  v-loading="!show">
    <el-row class="title" type="flex" justify="space-between" align="middle">
      <el-col class="title-left">
        <h3>成交分布</h3>
      </el-col>
      <el-col class="title-right">
        <p>属性成交分布</p>
      </el-col>
    </el-row>
    <el-row class="navlist" style="height:50px;backgroundColor:#E5E9F2;padding-top:2px;">
      <el-col class="small">
        选择时间:
        <el-date-picker :picker-options="pickerOption" v-model="value1" size='small' type="month" @change="getListGroup"></el-date-picker>
      </el-col>
      <el-col class="small">
        选择类目：
        <el-select v-model="value0" size='small' @change="getListGroup">
          <el-option v-for="item in options0" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-col>
      <el-col>
        <div class="small-group">
          <div> 选择属性：</div>
          <span v-for="item in listgroup">
          <a :class="{bold:activeName==item}"  @click="inputchange(item)">{{item}}</a>|
        </span>
        </div>
      </el-col>
    </el-row>
    <el-row v-show="show" style="backgroundColor:#F9FAFC;height:100%;">
      <el-col style="width:52%;margin:2% 1% 2% 2%;backgroundColor:#FFF;">
        <IEcharts id="echart" :option="option" :resizable="true"></IEcharts>
        <el-table id="SYJ_Table" :data="tableData">
          <el-table-column prop="属性值" label="属性值" align="right" header-align="right">
          </el-table-column>
          <el-table-column prop="成交量" label="成交量" align="right" header-align="right">
          </el-table-column>
          <el-table-column prop="销售额" label="销售额" align="right" header-align="right">
          </el-table-column>
          <el-table-column prop="高质宝贝数" label="高质宝贝数" align="right" header-align="right">
          </el-table-column>
        </el-table>
      </el-col>
      <el-col style="width:40%;margin:2% 2% 2% 1%;backgroundColor:#FFF;border-radius:2px;">
        <IEcharts style="width:100%;height:1200px;border:1px solid #D3DCE6;" :option="option1" :resizable="true"></IEcharts>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  import IEcharts from 'vue-echarts-v3/src/full.vue';
  import 'echarts/lib/chart/bar';
  import 'echarts/lib/chart/pie';
  export default {
    components: {
      IEcharts
    },
    data() {
      return {
        show: false,
        activeName: '',
        pickerOption: {
          disabledDate(time) {
            if (time > Date.parse('2017-05-01') || time < Date.parse('2011-04-01')) {
              return true;
            } else {
              return false;
            }
          }
        },
        value0: '牛仔裤',
        value1: '2017-05',
        options0: [{
          label: '类目：牛仔裤',
          value: '牛仔裤'
        }, {
          label: '类目：休闲裤',
          value: '休闲裤'
        }, {
          label: '类目：打底裤',
          value: '打底裤'
        }, {
          label: '类目：半身裙',
          value: '半身裙'
        }, {
          label: '类目：大码女装',
          value: '大码女装'
        }, {
          label: '类目：连衣裙',
          value: '连衣裙'
        }, {
          label: '类目：棉裤羽绒裤',
          value: '棉裤羽绒裤'
        }, {
          label: '类目：西装裤正装裤',
          value: '西装裤正装裤'
        }, {
          label: '类目：成交量分布',
          value: '成交量分布'
        }],
        options1: {},
        listgroup: {},
        tableData: [],
        option: {
          title: {
            text: ''
          },
          tooltip: {},
          legend: {
            data: [],
            selectedMode: 'single',
            selected: {}
          },
          yAxis: {
            type: 'category',
            data: []
          },
          grid: {
            left: '10%'
          },
          xAxis: {
            type: 'value'
          },
          color: ['#516b91', '#59c4e6', '#edafda'],
          series: []
        },
        option1: {
          title: {
            text: '',
            subtextStyle:{
              fontSize:16
            },
            itemGap:200,
            subtext: ' 成\n 交\n 量\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n 销\n 售\n 额\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n  高\n  质\n  宝\n  贝\n  数'
          },
          tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
          },
          legend: {
            left: 'right',
            align: 'right',
            formatter: function (name) {
              return name
            },
            orient: 'vertical',
            data: []
          },
          color: ['#59c4e6', '#edafda', '#516b91', '#93b7e3', '#a5e7f0', '#cbb0e3'],
          series: [{
            name: '成交量',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: [],
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }]
        }
      }
    },
    created() {
      this.$http.get('pete/shop').then((response) => {
        this.listgroup = Object.keys(response.body.data).map(function (key) {
          return response.body.data[key];
        })
        if (this.activeName == '' || this.listgroup.indexOf(this.activeName) == -1) {
          this.activeName = this.listgroup[0]
        }
        this.inputchange(this.activeName)
      })
    },
    methods: {
      getListGroup() {
        var data1 = {
          "data_time": this.value1,
          "category": this.value0,
          "attribute": 'list'
        }
        var data = JSON.stringify(data1) //格式化数据
        this.show = false
        this.$http.post('pete/shop', {
          data
        }, {
          emulateJSON: true
        }).then((response) => {
          
          this.listgroup = Object.keys(response.body.data).map(function (key) {
            return response.body.data[key];
          })
          if (this.activeName == '' || this.listgroup.indexOf(this.activeName) == -1) {
            this.activeName = this.listgroup[0]
          }
          this.inputchange(this.activeName)
        })
      },
      inputchange(prop) {
        this.activeName = prop
        var data1 = {
          "data_time": this.value1,
          "category": this.value0,
          "attribute": prop,
          "variable": 'all'
        }
        var data = JSON.stringify(data1) //格式化数据
        this.$http.post('pete/shop', {
          data
        }, {
          emulateJSON: true
        }).then((response) => {
          if (response.body.message == "ok") {
            var Items = response.body.data
            this.option.title.text = this.option1.title.text = this.activeName

            //图表数据处理

            this.option.yAxis.data = Object.keys(Items).map(function (key) {
              return Items[key]['属性值']
            }).reverse()

            // 将表封装为函数

            var option = { //series参数设置
              name: ['成交量', '销售额', '高质宝贝数'], //参数名称
              data: Items, //参数数据
              type: 'bar' //参数类型
            }
            this.option.series = this.getItem(option)
            this.option.legend.data = ['成交量', '销售额', '高质宝贝数']
            var option1 = {
              name: ['成交量', '销售额', '高质宝贝数'], //设置参数名称
              data: Items, //参数数据
              type: 'pie' //参数类型
            }
            this.option1.series = this.getItem(option1)

            //表格数据处理
            this.tableData = Object.keys(Items).map(function (key) {
              return Items[key]
            })
            var target = document.getElementById('echart')
            target.style.height = this.tableData.length * 23.94 + 126.63 + 'px'
            this.show = true;
          }
        })
      },
      getItem(option) {
        var arr = Array()
        if (option.type == 'bar') { //柱形图执行
          for (var j = 0; j < option.name.length; j++) {
            (function () {
              var _this = Object()
              _this.data = []
              _this.name = option.name[j]
              _this.type = option.type
              _this.barWidth = 20
              _this.label = {
                normal: {
                  show: true,
                  position: 'right',
                  formatter: function (item) {
                    var num = Object.keys(option.data).map(function (key) {
                      return option.data[key][_this.name]
                    }).reduce(function (a, b) {
                      return a + b;
                    }, 0)
                    return item.data + '(' + ((item.data * 100) / num).toFixed(2) + '%)'
                  }
                }
              }
              for (var i in option.data) {
                _this.data.push(option.data[i][_this.name])
              }
              _this.data.reverse()
              arr.push(_this)
            })(j) //造成的for循环闭包问题j值得到的不是期待值
          }
        } else if (option.type == 'pie') { //饼图执行
          var arr = Array()
          for (var j = 0; j < option.name.length; j++) {
            (function () {
              var _this = Object()
              _this.data = []
              _this.radius = 120
              _this.name = option.name[j]
              _this.type = option.type
              _this.label = {
                normal: {
                  formatter: "{b}:{d}%",
                  textStyle:{
                    fontSize:14
                  }
                }
              }
              var y, x;
              if (j == 0) {
                x = '50%'
                y = '20%'
              } else if (j == 1) {
                x = '50%'
                y = '50%'
              } else if (j == 2) {
                x = '50%'
                y = '80%'
              }
              _this.center = [x, y]
              _this.data = Object.keys(option.data).map(function (key) {
                var value = option.data[key][_this.name]
                var name = option.data[key]['属性值']
                return {
                  value: value,
                  name: name
                }
              })
              var afterThird = _this.data.splice(3).map(function (item) {
                return item.value
              }).reduce(function (a, b) {
                return a + b;
              }, 0)
              if (!afterThird == 0) {
                _this.data.push({
                  name: '其它',
                  value: afterThird
                })
              }
              arr.push(_this)
            })(j) //造成的for循环闭包问题j值得到的不是期待值
          }
          this.option1.legend.data = Object.keys(option.data).map(function (key) {
            if (key < 3) {
              return option.data[key]['属性值']
            } else {
              return '其它'
            }

          })
        } else { //
          throw 'not suport this chart type,only "bar and pie"'
        }
        return arr;
      }
    }
  }

</script>
<style>
  #echart {
    border: 1px solid #D3DCE6;
    border-radius: 2px;
    display: inline-block;
    margin-bottom:2%;
    width: 100%;
    height: 100%;
  }

  .bold {
    font-weight: bold;
    font-size: 15px;
    border-radius: 2px;
  }

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

  #SYJ_Table {
    
    width: 100%;
    font-size: 12px;
  }

  #SYJ_Table .el-table__header-wrapper table.el-table__header thead tr th {
    background: #59c4e6;
  }

  #SYJ_Table .el-table__fixed-header-wrapper thead div,
  #SYJ_Table .el-table__header-wrapper thead div {
    background: #59c4e6;
    color: #FFFFFF;
    font-size: 18px;
    font-weight: normal;
  }

  #SYJ_Table.el-table td.is-right,
  #SYJ_Table.el-table th.is-right {
    padding-right: 30px;
  }

</style>
