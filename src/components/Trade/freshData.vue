<template lang="">
  <div >
    <main class="main" style="color:#fff;background: #121212;">
      <div class="left">
        <div>
          <nav class="nav_tabs">
            <div class="tabs_title">
              <span :style="[tabItem===index ? active:'']" v-for="(item,index) in navTabs" @click="tabToggle(index)">{{item}}</span>
           </div>
            <div class="tabs_content-top">
              <span :style="[retime===index ? isCorver : normal]" v-for="(item,index) in timeReview" @click="timeToggle(index)">{{item}}</span>
            </div>
             <div class="tabs_content-bottom">
              <span>开始运动</span>
            </div>
          </nav>
          <section>
            <IEcharts style="width:400px;height:300px;" :option="bar" :resizable="true"></IEcharts>
          </section>
        </div>
      </div>
      <div class="center">
        <IEcharts style="width:400px;height:300px;" :option="line" :resizable="true"></IEcharts>
      </div>
      <div class="right">
        <IEcharts style="width:400px;height:300px;" :option="pie" :resizable="true"></IEcharts>
      </div>
    </main>
  
  </div>
</template>
<script>
  import IEcharts from 'vue-echarts-v3/src/full.vue'
  import echarts from 'echarts'
  export default {
    components: {
      IEcharts
    },
    data() {
      return {
        tabItem:0,
        navTabs:['运动','轨迹','消耗'],
        retime:0,
        active:{
          color: '#FF0435',
          borderBottom:'2px solid #FF0435'
        },
        normal:{
          color:'#FF0435'
        },
        isCorver:{
          color:'#fff',
          background:'#FF0435'
        },
        timeReview:['今天','历史'],
        bar: {
          title: {
            text: '当日收入',
            subtext: '实时'
          },
          xAxis: {
            data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
            axisLabel: {
              inside: true,
              textStyle: {
                color: '#fff'
              }
            },
            axisTick: {
              show: false
            },
            axisLine: {
              show: false
            },
            z: 10
          },
          yAxis: {
            axisLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            axisLabel: {
              textStyle: {
                color: '#999'
              }
            }
          },
          dataZoom: [{
            type: 'inside'
          }],
          series: [{
            type: 'bar',
            itemStyle: {
              normal: {
                color: new echarts.graphic.LinearGradient(
                  0, 0, 0, 1, [{
                      offset: 0,
                      color: '#FF0435'
                    },
                    {
                      offset: 0.5,
                      color: '#F6033D'
                    },
                    {
                      offset: 1,
                      color: '#CE025B'
                    }
                  ]
                )
              },
              emphasis: {
                color: new echarts.graphic.LinearGradient(
                  0, 0, 0, 1, [{
                      offset: 0,
                      color: '#CE025B'
                    },
                    {
                      offset: 0.7,
                      color: '#F6033D'
                    },
                    {
                      offset: 1,
                      color: '#FF0435'
                    }
                  ]
                )
              }
            },
            data: [122, 133, 334, 198, 123, 125, 220]
          }]
        },
        line: {
          tooltip: {
            trigger: 'axis',
            formatter: "{b}：运动 {c}km"
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          yAxis: {
            type: 'value',
            axisLabel: {
              formatter: '{value}  km'
            }
          },
          xAxis: {
            axisTick: {
              show: false
            },
            type: 'category',
            boundaryGap: false,
            data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
          },
          series: [{
            name: '历史',
            type: 'line',
            smooth: true,
            symbol: 'circle',
            lineStyle: {
              normal: {
                color: new echarts.graphic.LinearGradient(
                  0, 0, 1, 0, [{
                      offset: 0,
                      color: '#FF033F'
                    },
                    {
                      offset: 0.5,
                      color: '#EB0536'
                    },
                    {
                      offset: 1,
                      color: '#D6015E'
                    }
                  ]
                ),
                width: 4
              },
            },
            areaStyle: {
              normal: {
                color: new echarts.graphic.LinearGradient(
                  0, 0, 0, 1, [{
                      offset: 0,
                      color: '#FF0435'
                    },
                    {
                      offset: 0.5,
                      color: '#270A0F'
                    },
                    {
                      offset: 0.8,
                      color: '#0E0A0B'
                    }
                  ]
                )
              }
            },
            data: ['10', '20', '20', '30', '35', '27', '20']
          }]
        },
        pie: {
          series: [{
            name: '今日已走',
            type: 'pie',
            radius: ['60%', '65%'],
            avoidLabelOverlap: false,
            label: {
              normal: {
                show: true,
                position: 'center',
                textStyle: {
                  color: '#fff',
                  fontSize: '80'

                },
                formatter: ' {c}'
              }
            },
            itemStyle: {
              normal: {
                color: new echarts.graphic.LinearGradient(
                  1, 0, 0, 0, [{
                      offset: 0.4,
                      color: '#FF033F'
                    },
                    {
                      offset: 1,
                      color: '#0E8BFF'
                    }
                  ]
                )
              }
            },
            silent: true,
            data: [{
              value: 335,
              name: '今日已走'
            }]
          }]
        }
      }
    },
    mounted() {

      console.log(IEcharts)

    },
    methods:{
      tabToggle(index){
      this.tabItem=index
      },
      timeToggle(index){
        console.log(index)
       this.retime=index
      }
    }
  }
</script>
<style>
  .main {
    position: relative;
    height: 60vh;
  }

  .left {
    width: 25%;
    height: 100%;
    display: inline-block;
  }

  .center {
    width: 45%;
    height: 100%;
    display: inline-block;
  }

  .right {
    width: 25%;
    height: 100%;
    display: inline-block;
  }

  .show_slider {
    text-align: center;
    width: 100%;
    border: 0px solid #FF0435;
  }
  .nav_tabs .tabs_title{
    text-align:center;
  }
  .nav_tabs .tabs_content-top{
    text-align:center;
    position:relative;
    padding:8% 30%;
    font-size:12px;
  }
   .nav_tabs .tabs_content-top span{
   display:inline-block;
    width:calc(50% - 2px);
   line-height:24px;
    border:1px solid #FF0435;
   }
 .nav_tabs .tabs_content-top span:first-child{
   border-top-left-radius: 12px;
   border-bottom-left-radius: 12px;
 
 }
  .nav_tabs .tabs_content-top span:last-child{
   border-top-right-radius: 12px;
   border-bottom-right-radius: 12px;
 }
.nav_tabs .tabs_title span{
  display: inline-block;
  width:10%;
  margin:auto 5%;
  text-align:center;
  line-height:5vh;
}
.tabs_content-bottom{
  height:50px;
padding:3% 30%;
text-align:center;
}
.tabs_content-bottom span{
  display:inline-block;
  line-height:40px;
  border:1px solid #FF0435;
  width:100%;
  border-radius:20px;
  background:linear-gradient(to right,#FF0435, #D6015E);
}

</style>
