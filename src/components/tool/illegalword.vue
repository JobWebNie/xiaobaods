<template>
  <div class="compare">
    <el-row class="title" type="flex" justify="space-between" align="middle">
      <el-col>
        <h3>2017年淘宝广告违禁词检测</h3>
      </el-col>
      <el-col class="title-right">
      </el-col>
    </el-row>
    <br>
    <br>
    <el-row type="flex" justify="space-around">
      <el-col :span="9">
        <el-input class="compare-along" type="textarea" placeholder="请输入内容" v-on:change="dispathBlur()" v-model.trim="value" resize="none"></el-input>
      </el-col>
      <el-col :span="9" class="compare-beyond">
        <span v-for="item in myData" v-bind:style="{color:item.style}">{{item.value}}</span>
      </el-col>
    </el-row>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        value: "",
        rule: /最(佳|具|爱|赚|优|好|大|高级|高档|高|奢侈|低级|低价|低|底|便宜|流行|受欢迎|时尚|聚拢|符合|舒适|先进|先|后|新科技|新科学|新)|((中国|全网|国际|国内|全球级|独家|国家级|销量|排名|国家|全球|宇宙级|世界级|绝对|精确|顶级)|(NO.1|No.1|no.1|TOP.1|Top.1|top.1|第一|唯一|独一|首个|首选|首发|首次|首款|首家)|(一流|仅此一天|仅此一次|仅此一款|一波))|(史无前例|前无古人|永久|万能|祖传|特效|无敌|纯天然|100%|高档|正品|真皮|超赚|精准|大牌|金牌|名牌|王牌|领袖品牌|领先|领导者|缔造者|创领品牌|上市|巨星|著名|掌门人|至尊|巅峰|奢侈|优秀|资深|领袖|之王|王者|冠军|老字号|驰名商标|特供|专供|免检|检测|免抽检|推荐|就没|再不抢就|疯抢|抢疯|卖疯|抢购|抢爆|秒杀|有惊喜|点击|领奖|恭喜|获奖|免单|领取奖品|获取|最)/g,
        myData: []
      }
    },
    methods: {
      dispathBlur() {
        this.myData = []
        var string = this.value
        string.match(this.rule)
        string.replace(this.rule, '♫$&♀').split('♀').map((item) => {
          var _item0 = item.split('♫')[0]
          var _item1 = item.split('♫')[1]
          this.myData.push({
            'style': 'black',
            'value': _item0
          }, {
            'style': 'red',
            'value': _item1
          })
        })
      }
    }
  }

</script>
<style>
  .compare {
    height: 100vh;
  }

  .compare .el-textarea__inner {
    height: 80vh;
  }
  .compare-beyond{
    border:1px solid #D3DCE6;
    padding: 5px 7px;
    font-size:14px;
    font-family:monospace;
    line-height:1.5;
    white-space: pre-wrap;
    word-wrap:break-word;
    height:80vh;
    overflow:auto;
  }

</style>
