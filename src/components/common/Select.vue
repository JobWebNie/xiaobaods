<template>
  <div style="float:left;border:1px dotted #999;" @mouseenter="interToMakeSelectDown" @mouseleave.self="leaveToMakeSelectUp">
    <a href="">{{label}}</a>
    <i class="el-icon-arrow-down"></i>
    <commonOption v-show="show" :productLists="productLists"  v-on:selectOption="selctTitleReceive"></commonOption>
  </div>
</template>
<script>
import commonOption from './Option.vue';
export default {
    components: {
        commonOption
    },
    props:{
        splitNumber:{
        type:Number,
        default:6
        }
    },
    data() {
        return {
           show:false,
           label:'',
           productLists:[['第一','第二','第三','第四','第五','第六'],['第七','第八','第九','第十','第十一','第十二']]
        }
    },
    mounted(){
        this.selctTitleReceive()
    },
    methods:{
        selctTitleReceive(v) {
           this.label = v ? v : this.productLists[0][0]
        },
        interToMakeSelectDown(){
            console.log('hover')
            this.show = true
        },
        leaveToMakeSelectUp(){
            console.log('leaver')
            this.show = false
        }
    }
}
</script>